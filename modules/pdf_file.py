import mimetypes
import pdf2image
import numpy as np
import cv2
import logging
import os
from PIL import Image
import tempfile

logger = logging.getLogger(__name__)

#tempdir = tempfile.TemporaryDirectory().name
#tempdir = 'Users/simonthompson/scratch/temp'

class ConsentForm:
    """class for an instance of a consent form on S3 buckets, gets initiated with an S3 object"""

    def __init__(self, o, file_id):

        def checkMimeType(f):
            """get file mime type"""
            logger.debug('Checking mime type for file_id %s' % self.file_id)
            return(mimetypes.guess_type(f))

        def toGray(i):
            """convert image to grayscale"""
            logger.debug('Received call to toGray for file_id %s' % self.file_id)
            return(cv2.cvtColor(i, cv2.COLOR_BGR2GRAY))
        
        def pdfToImage(f):
            """get images from pdf files, deletes the original pdf"""
            logger.debug('Converting %s to images for file_id %s' % (f, self.file_id))
            try:
                i = pdf2image.convert_from_path(f)
                o = [toGray(np.array(x)) for x in i]
                os.remove(f)
            except (AttributeError, pdf2image.exceptions.PDFPageCountError) as e:
                logger.warning('Image conversion failed for %s - %s' % (f, e))
                o = None
            return(o)

        def dlToTemp(o):
            """download file from S3 to temp"""
            f = tempfile.NamedTemporaryFile(delete = False)
            o.download_fileobj(f)
            return(f.name)

        self.path = dlToTemp(o)
        self.file_id = file_id
        self.mime_type = checkMimeType(self.path)[0]
        self.pages = pdfToImage(self.path)
        self.valid_file = self.mime_type in ['application/pdf'] and self.pages is not None

    def RemoveEmpties(self, minsd = 10):
        """remove pages that look like they're empty, sd of pixels is below certain amount"""
        logger.debug('Received call to RemoveEmpties for file_id %s' % self.file_id)
        empty_pages = [np.std(i) < minsd for i in self.pages]
        logger.info('Removing %s pages' % sum(empty_pages))
        self.pages = [i for (i, e) in zip(empty_pages, self.pages) if not e]

    def RotateLandscapePages(self):
        """rotate any landscape pages"""
        logger.debug('Received call to RotateLandscapePages for file_id %s' % self.file_id)
        for i in range(len(self.pages)):
            if self.pages[i].shape[1] > self.pages[i].shape[0]:
                logger.debug('Rotating page number %s' % (i+1))
                self.pages[i] = np.rot90(self.pages[i])

    def ExportPages(self, root_folder):
        """save pages as images to given folder"""
        logger.debug('Received call to ExportImages for file_id %s' % self.file_id)
        # create the folder
        f = root_folder + '/' + self.file_id
        self.image_folder = f
        self.image_filepaths = []
        try:
            os.mkdir(f)
            logger.debug('New folder created %s' % f)
        except FileExistsError:
            logger.warning('Folder already exists %s' % f)
        # save each page
        for i in range(len(self.pages)):
            fn = f + '/' + str(self.file_id) + '_' + str(i + 1) + '.png'
            try:
                logger.debug('Exporting %s' % fn)
                Image.fromarray(self.pages[i]).save(fn)
                self.image_filepaths.append(fn)
            except:
                logger.warning('Export of %s failed' % fn)

    def __repr__(self):
        return('<Consent Form at %s>' % self.path)

