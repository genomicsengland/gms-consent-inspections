import mimetypes
import pdf2image
import numpy as np
import cv2
import logging
import os
from botocore.exceptions import ClientError
from PIL import Image
import tempfile
from models import gms_consent_db

logger = logging.getLogger(__name__)

#tempdir = tempfile.TemporaryDirectory().name
#tempdir = 'Users/simonthompson/scratch/temp'

class ConsentForm:
    """class for an instance of a consent form on S3 buckets, gets initiated with an S3 object, and an attachment object"""

    def __init__(self, o, attachment):

        def checkMimeType():
            """get file mime type"""
            logger.debug('Checking mime type for file_id %s' % self.attachment.file_id)
            return mimetypes.guess_type(self.path)

        def toGray(i):
            """convert image to grayscale"""
            logger.debug('Received call to toGray for file_id %s' % self.attachment.file_id)
            return cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)

        def identifyEmpties(minsd = 10):
            """identify pages that are likely empty"""
            logger.debug('Received call to identifyEmpties for file_id %s' % self.attachment.file_id)
            self.empty_pages = [np.std(i) < minsd for i in self.pages]
        
        def pdfToImage():
            """get images from pdf files, deletes the original pdf"""
            logger.debug('Converting images for file_id %s' % self.attachment.file_id)
            try:
                i = pdf2image.convert_from_path(self.path)
                o = [toGray(np.array(x)) for x in i]
                os.remove(self.path)
                self.pages = o
                identifyEmpties()
                rotateLandscapePages()
            except (AttributeError, pdf2image.exceptions.PDFPageCountError) as e:
                logger.warning('Image conversion failed for %s - %s' % (self.attachment.file_id, e))
                self.errors.append('image_conversion')

        def rotateLandscapePages():
                """rotate any landscape pages"""
                logger.debug('Received call to RotateLandscapePages for file_id %s' % self.attachment.file_id)
                for i in range(len(self.pages)):
                    if self.pages[i].shape[1] > self.pages[i].shape[0]:
                        logger.debug('Rotating page number %s' % (i+1))
                        self.pages[i] = np.rot90(self.pages[i])

        def processFile():
            """download file from S3 to temp and convert to image"""
            f = tempfile.NamedTemporaryFile(delete = False)
            try:
                self.s3_object.download_fileobj(f)
                self.path = f.name
                logger.info('S3Object downloaded to %s' % self.path)
                self.mime_type = checkMimeType()[0]
            except ClientError as e:
                logger.warning('Failed to download file_id %s - %s' % (self.attachment.file_id, e))
                self.errors.append('download')
            pdfToImage()

        def extractUID():
            """extract the uids from filename"""


        def exportPages(root_folder):
            """save pages as images to given folder"""
            logger.debug('Received call to ExportImages for file_id %s' % self.attachment.file_id)
            # create the folder
            f = root_folder + '/' + str(self.attachment.file_id)
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
                except:
                    logger.warning('Export of %s failed' % fn)

        self.s3_object = o
        self.attachment = attachment
        self.errors = []
        self.pages = []
        processFile()
        exportPages('/Users/simonthompson/scratch')

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

    def __repr__(self):
        return('<Consent Form at %s>' % self.path)

