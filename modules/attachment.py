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
from modules import s3
import local_config
import urllib.parse

logger = logging.getLogger(__name__)

class Attachment:
    """An attachment present within the GMS GR database, comprising a SQLAlchemy Attachment object and it's matching S3 Object

    Attributes:
        gr_attachment: an Instance of gr_db.Attachment
        s3_object: an S3 Object
        index_attachment: an Instance of gms_consent_db.Attachment
        path: the location of the file download, is deleted once file is successfully processed
        pages: a list of grayscale numpy arrays generated from the document scans
        empty_pages: boolean list showing which of the pages is thought to be empty 
        errored: boolean to record if there were errors during processing
        errors: list of errors that have accumalated over the course of document processing
        image_folder: the path to the folder holding the png image for each page of the document
        image_filepaths: list of file paths to the png images for each page of the document
        person_name: the name of the patient as given in the GR database
        dob: the date of birth of the patient as given in the GR database
    """

    def __init__(self, gr_attachment, session):

        def logError(e):
            self.errored = True
            self.errors.append(e)

        def createS3Object():
            """create S3 object form the filepath"""
            logger.debug('Received call to createS3Object')
            try:
                f = self.gr_attachment.attachment_url
                b, k = f.split('/')
                return s3.createS3Obj(b, k + 'fsdjkl')
            except Exception as e:
                logError('sourcing file from s3 - %s' % e)

        def addToIndex():
            a = gms_consent_db.Attachment(
                gr_attachment_uid = gr_attachment.uid,
                s3_bucket = self.s3_object.bucket_name,
                s3_key = self.s3_object.key
            )
            session.add(a) 
            session.flush()
            return a

        def checkMimeType():
            """get file mime type"""
            logger.debug('Received call to checkMimeType for attachment_id %s' % self.attachment_id)
            return mimetypes.guess_type(self.path)

        def toGray(i):
            """convert image as np array to grayscale"""
            logger.debug('Received call to toGray for attachment_id %s' % self.attachment_id)
            return cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)

        def identifyEmpties(minsd = 10):
            """identify pages that are likely empty"""
            logger.debug('Received call to identifyEmpties for attachment_id %s' % self.attachment_id)
            self.empty_pages = [np.std(i) < minsd for i in self.pages]

        def rotateLandscapePages():
            """rotate any landscape pages"""
            logger.debug('Received call to rotateLandscapePages for attachment_id %s' % self.attachment_id)
            for i in range(len(self.pages)):
                if self.pages[i].shape[1] > self.pages[i].shape[0]:
                    logger.debug('Rotating page number %s' % (i+1))
                    self.pages[i] = np.rot90(self.pages[i])
        
        def convertToImage():
            """get grayscale images from pdf files, identify empties and rotate any landscape pages"""
            logger.debug('Received call to convertToImage for attachment_id %s' % self.attachment_id)
            try:
                i = pdf2image.convert_from_path(self.path)
                o = [toGray(np.array(x)) for x in i]
                self.pages = o
                identifyEmpties()
                rotateLandscapePages()
                logger.info('Image conversion successful for attachment_id %s; %s pages' % (self.attachment_id, len(self.pages)))
            except (AttributeError, pdf2image.exceptions.PDFPageCountError) as e:
                logger.warning('Image conversion failed for attachment_id %s - %s' % (self.attachment_id, self.path))
                logError('image_conversion')

        def deleteFile():
            """deletes the tempfile where the s3 object was downloaded to and it's reference"""
            logger.debug('Received call to deleteFile for attachment_id %s - %s' % (self.attachment_id, self.path))
            os.remove(self.path)
            del self.path

        def exportPages():
            """save pages as images to given folder"""
            logger.debug('Received call to ExportImages for attachment_id %s' % self.attachment_id)
            # create the folder
            f = '%s/%s' % (local_config.image_store_dir, self.attachment_id)
            self.image_folder = f
            self.image_filepaths = []
            try:
                os.mkdir(f)
                logger.debug('New folder created %s' % f)
            except FileExistsError:
                logger.warning('Folder already exists %s' % f)
            # save each page
            for i in range(len(self.pages)):
                fn = f + '/' + str(self.attachment_id) + '_' + str(i + 1) + '.png'
                try:
                    logger.debug('Exporting %s' % fn)
                    Image.fromarray(self.pages[i]).save(fn)
                    self.image_filepaths.append(fn)
                except Exception as e:
                    logger.warning('Export of %s failed - %s' % (fn, e))
                    logError('image_export')

        def processFile():
            """download file from S3 to temp and convert to image"""
            logger.debug('Received call to processFile for attachment_id %s' % self.attachment_id)
            f = tempfile.NamedTemporaryFile(delete = False)
            try:
                self.s3_object.download_fileobj(f)
                self.path = f.name
                self.mime_type = checkMimeType()[0]
            except ClientError as e:
                logger.warning('Failed to download attachment_id %s - %s' % (self.attachment_id, self.path))
                logError('download')
            if hasattr(self, 'path'):
                # if we've got a file path then attempt to convert to images and export
                convertToImage()
                exportPages()
            if not self.errored:
                # if we didn't pick up any errors then can delete the file
                deleteFile()

        def extractUID():
            """extract the uids from filename"""
            logger.debug('Received call to extractUID for attachment_id %s' % self.attachment_id)
            s = self.s3_object.key.split('_')
            self.index_attachment.patient_uid = s[0]
            self.index_attachment.referral_uid = s[1]

        # do some initial assignment and creation of attributes to reference later
        self.errors = []
        self.errored = False
        self.gr_attachment = gr_attachment
        self.s3_object = createS3Object()
        self.index_attachment = addToIndex()
        self.attachment_id = self.index_attachment.attachment_id
        self.pages = []
        self.person_name = None
        self.dob = None
        # do processing of file - download, convert to image, export
        processFile()
        # match to patient and referral
        extractUID()

    def updateDB(self):
        """add relevant rows to database"""
        self.index_attachment.images = []
        self.index_attachment.errors = []
        try:
            for i in range(len(self.pages)):
                self.index_attachment.images.append(gms_consent_db.Image(
                    path = self.image_filepaths[i],
                    page_number = i + 1,
                    page_empty = self.empty_pages[i]
                ))
        except:
            logger.info('cannot add pages')
        try:
            for i in range(len(self.errors)):
                self.index_attachment.errors.append(gms_consent_db.Error(
                    error_type = self.errors[i]
                ))
        except:
            logger.info('cannot add errors')

    def extractParticipantInfo(self, session):
        """Get participant info from GR database for the form's owner"""
        logger.debug('Received call to extractParticipantInfo for attachment_id %s; patient_uid %s' % (self.attachment_id, self.index_attachment.patient_uid))
        pax = session.query(gr_db.Patient.person_uid,
                      gr_db.Patient.patient_date_of_birth).\
            filter(gr_db.Patient.uid == self.index_attachment.patient_uid).first()
        per = session.query(gr_db.Person.person_first_name,
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
        logger.debug('Received call to cropImageArea for attachment_id %s' % self.attachment_id)
        # get sizes and resize factors
        img = self.pages[p - 1]
        ih,iw = img.shape
        f = iw / fw
        # crop out the relevant part of the image
        cimg = img[int(ih * y):int(ih*(y+h)), int(iw * x):int(iw * (x + w))]
        # return a resized version of the crop
        return cv2.resize(cimg, dsize = (int(ih / f), fw))

    def createFaultTicketURL(self):
        """create url to create """
        d = {
            "reporter" : "sthompson",
            "issuetype" : "3",
            "assignee" : "sthompson",
            "summary" : 'Consent Form Fault for File %s' % self.attachment_id,
            "description" : "Something has gone wrong with this file.\n Original location %s/%s" % (self.s3_object.bucket_name, self.s3_object.key),
            "pid" : "11438"
        }
        url = '%s/secure/CreateIssueDetails!init.jspa?%s' % (local_config.jira_config['url'], urllib.parse.urlencode(d))
        return url

    def __repr__(self):
        return('<Attachment - ID %s>' % self.attachment_id)

