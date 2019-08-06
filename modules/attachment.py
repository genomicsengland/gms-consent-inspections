# provides an Attachment class for getting and processing GR attachments
import mimetypes
import pdf2image
import numpy as np
import cv2
import logging
import os
from botocore.exceptions import ClientError
from PIL import Image
import tempfile
from models import gms_consent_db, gr_db
import local_config

logger = logging.getLogger(__name__)

class Attachment:
    """an instance of a attachment on S3 buckets, gets initiated with an S3 object, and a gr_db.attachment object"""

    def __init__(self, s3_object, attachment):

        def checkMimeType():
            """get file mime type"""
            logger.debug('Received call to checkMimeType for file_id %s' % self.attachment.file_id)
            return mimetypes.guess_type(self.path)

        def toGray(i):
            """convert image as np array to grayscale"""
            logger.debug('Received call to toGray for file_id %s' % self.attachment.file_id)
            return cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)

        def identifyEmpties(minsd = 10):
            """identify pages that are likely empty"""
            logger.debug('Received call to identifyEmpties for file_id %s' % self.attachment.file_id)
            self.empty_pages = [np.std(i) < minsd for i in self.pages]

        def rotateLandscapePages():
            """rotate any landscape pages"""
            logger.debug('Received call to rotateLandscapePages for file_id %s' % self.attachment.file_id)
            for i in range(len(self.pages)):
                if self.pages[i].shape[1] > self.pages[i].shape[0]:
                    logger.debug('Rotating page number %s' % (i+1))
                    self.pages[i] = np.rot90(self.pages[i])
        
        def convertToImage():
            """get grayscale images from pdf files, identify empties and rotate any landscape pages"""
            logger.debug('Received call to convertToImage for file_id %s' % self.attachment.file_id)
            try:
                i = pdf2image.convert_from_path(self.path)
                o = [toGray(np.array(x)) for x in i]
                self.pages = o
                identifyEmpties()
                rotateLandscapePages()
                logger.info('Image conversion successful for file_id %s; %s pages' % (self.attachment.file_id, len(self.pages)))
            except (AttributeError, pdf2image.exceptions.PDFPageCountError) as e:
                logger.warning('Image conversion failed for %s - %s' % (self.attachment.file_id, e))
                self.errors.append('image_conversion')

        def deleteFile():
            """deletes the tempfile where the s3 object was downloaded to and it's reference"""
            logger.debug('Received call to deleteFile for file_id %s - %s' % (self.attachment.file_id, self.path))
            os.remove(self.path)
            del self.path

        def exportPages():
            """save pages as images to given folder"""
            logger.debug('Received call to ExportImages for file_id %s' % self.attachment.file_id)
            # create the folder
            f = '%s/%s' % (local_config.image_store_dir, self.attachment.file_id)
            self.image_folder = f
            self.image_filepaths = []
            try:
                os.mkdir(f)
                logger.debug('New folder created %s' % f)
            except FileExistsError:
                logger.warning('Folder already exists %s' % f)
            # save each page
            for i in range(len(self.pages)):
                fn = f + '/' + str(self.attachment.file_id) + '_' + str(i + 1) + '.png'
                try:
                    logger.debug('Exporting %s' % fn)
                    Image.fromarray(self.pages[i]).save(fn)
                    self.image_filepaths.append(fn)
                except Exception as e:
                    logger.warning('Export of %s failed - %s' % (fn, e))
                    self.errors.append('image_export')

        def processFile():
            """download file from S3 to temp and convert to image"""
            logger.debug('Received call to processFile for file_id %s' % self.attachment.file_id)
            f = tempfile.NamedTemporaryFile(delete = False)
            try:
                self.s3_object.download_fileobj(f)
                self.path = f.name
                self.mime_type = checkMimeType()[0]
            except ClientError as e:
                logger.warning('Failed to download file_id %s - %s' % (self.attachment.file_id, e))
                self.errors.append('download')
            if hasattr(self, 'path'):
                # if we've got a file path then attempt to convert to images and export
                convertToImage()
                exportPages()
            if len(self.errors) == 0:
                # if we didn't pick up any errors then can delete the file
                deleteFile()

        def extractUID():
            """extract the uids from filename"""
            logger.debug('Received call to extractUID for file_id %s' % self.attachment.file_id)
            s = self.s3_object.key.split('_')
            self.patient_uid = s[0]
            self.referral_uid = s[1]

        # do some initial assignment and creation of attributes to reference later
        self.s3_object = s3_object
        self.attachment = attachment
        self.errors = []
        self.pages = []
        self.person_name = None
        self.dob = None
        # do processing of file - download, convert to image, export
        processFile()
        # match to patient and referral
        extractUID()

    def addToDB(self, s):
        """add relevant rows to database, s is a sqlalchemy session"""
        self.attachment.s3_object = gms_consent_db.s3Object(
                s3_bucket = self.s3_object.bucket_name,
                s3_key = self.s3_object.key,
                images = []
            )
        self.attachment.errors = []
        try:
            for i in range(len(self.pages)):
                self.attachment.s3_object.images.append(gms_consent_db.fileImage(
                    path = self.image_filepaths[i],
                    page_number = i + 1,
                    page_empty = self.empty_pages[i]
                ))
        except:
            logger.info('cannot add pages')
        try:
            for i in range(len(self.errors)):
                self.attachment.errors.append(gms_consent_db.error(
                    error_type = self.errors[i]
                ))
        except:
            logger.info('cannot add errors')

    def extractParticipantInfo(self, s):
        """Get participant info from GR database for the form's owner"""
        logger.debug('Received call to extractParticipantInfo for file_id %s; patient_uid %s' % (self.attachment.file_id, self.patient_uid))
        pax = s.query(gr_db.Patient.person_uid,
                      gr_db.Patient.patient_date_of_birth).\
            filter(gr_db.Patient.uid == self.patient_uid).first()
        per = s.query(gr_db.Person.person_first_name,
                      gr_db.Person.person_family_name).\
            filter(gr_db.Person.uid == pax[0]).first()
        if pax is not None and per is not None:
            logger.debug('Linked to person_uid %s' % pax[0])
            self.person_name = ('%s %s' % (per[0], per[1])).upper()
            self.dob = '{0:%Y-%m-%d}'.format(pax[1])
        else:
            self.errors.append('linking to participant')

    def cropImageArea(self, p, x, y, w, h, fw):
        """crop out a specific portion of a page, and return it to specific width and height
        p - page; x,y - top left corner as proportion of page width & height,
        w,h - proportion of page width and height to be included;
        fw - final width of image in pixels to be generated"""
        logger.debug('Received call to cropImageArea for file_id %s' % self.attachment.file_id)
        # get sizes and resize factors
        img = self.pages[p - 1]
        ih,iw = img.shape
        f = iw / fw
        # crop out the relevant part of the image
        cimg = img[int(ih * y):int(ih*(y+h)), int(iw * x):int(iw * (x + w))]
        # return a resized version of the crop
        return cv2.resize(cimg, dsize = (int(ih / f), fw))

    def __repr__(self):
        return('<Attachment - ID %s>' % self.attachment.file_id)

