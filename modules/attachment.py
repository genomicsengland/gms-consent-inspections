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
from models import tk_db, gr_db
from modules import s3
import local_config
import urllib.parse
import random

LOGGER = logging.getLogger(__name__)


class Attachment:
    """
    An attachment present within the GMS GR database, comprising a SQLAlchemy
    Attachment object and it's matching S3 Object

    Attributes:
        gr_attachment: an Instance of gr_db.Attachment
        s3_object: an S3 Object
        tk_db_attachment: an Instance of tk_db.Attachment
        path: the location of the file download, is deleted once file is
        successfully processed
        pages: a list of grayscale numpy arrays generated from the document
        scans
        empty_pages: boolean list showing which of the pages is thought to be
        empty
        errored: boolean to record if there were errors during processing
        errors: list of errors that have accumalated over the course of
        document processing
        image_folder: the path to the folder holding the png image for each
        page of the document
        image_filepaths: list of file paths to the png images for each page of
        the document
        person_name: the name of the patient as given in the GR database
        dob: the date of birth of the patient as given in the GR database
    """

    def __init__(self, gr_attachment, session):

        def log_error(e):
            """
            log an error and make the attachment 'errored'
            """

            LOGGER.debug('Error during processing of %s - %s',
                         self.gr_attachment.attachment_url, e)
            self.errored = True
            self.errors.append(e)

        def create_s3_object():
            """
            create S3 object from the filepath
            """

            LOGGER.debug('Received call to create_s3_object')

            try:

                f = self.gr_attachment.attachment_url
                b, k = f.split('/')

                return s3.create_s3_obj(b, k)

            except Exception as e:

                log_error('sourcing file from s3 - %s' % e)

        def add_to_db():
            """
            add the attachment to the tracker db
            :returns: tk_db.Attachment object flushed through db
            """

            # create the SQLAlchemy object
            a = tk_db.Attachment(
                uid=gr_attachment.uid,
                s3_bucket=self.s3_object.bucket_name,
                s3_key=self.s3_object.key,
                pages=[],
                errors=[]
            )

            # add then flush
            session.add(a)
            session.flush()

            return a

        def check_mime_type():
            """
            get file mime type for the current attachment
            """

            LOGGER.debug('Received call to check_mime_type for attachment_id %s',
                         self.attachment_id)

            return mimetypes.guess_type(self.path)

        def convert_to_gray(i):
            """
            convert image as np array to grayscale
            :params i: numpy array of image
            :returns: grayscale image
            """

            LOGGER.debug('Received call to convert_to_gray for attachment_id %s',
                         self.attachment_id)

            return cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)

        def identify_empty_pages(minsd=10):
            """
            identify pages that are likely empty
            :params minsd: cut-off standard deviation for pixel values to be
            considered empty
            """

            LOGGER.debug('Received call to identify_empty_pages for attachment_id %s',
                         self.attachment_id)

            # generates a boolean list for whether the page is empty or not
            self.empty_pages = [np.std(i) < minsd for i in self.pages]

        def rotate_landscape_pages():
            """
            rotate any landscape pages
            """

            LOGGER.debug('Received call to rotate_landscape_pages for attachment_id %s',
                         self.attachment_id)

            # process each page that is wider that it is tall
            for i in range(len(self.pages)):

                if self.pages[i].shape[1] > self.pages[i].shape[0]:

                    LOGGER.debug('Rotating page number %s', (i+1))

                    self.pages[i] = np.rot90(self.pages[i])
        
        def process_pdf_to_image():
            """
            get grayscale images from pdf files, identify empties and rotate
            any landscape pages
            """

            LOGGER.debug('Received call to process_pdf_to_image for attachment_id %s',
                         self.attachment_id)

            try:

                # convert pdf to images
                i = pdf2image.convert_from_path(self.path)

                # convert each image to a grayscale image
                self.pages = [convert_to_gray(np.array(x)) for x in i]

                # identify empty pages
                identify_empty_pages()

                # rotate any landscape pages
                rotate_landscape_pages()

                LOGGER.info('Image conversion successful for attachment_id %s; %s pages',
                            self.attachment_id, len(self.pages))

            except (AttributeError, pdf2image.exceptions.PDFPageCountError) as e:

                LOGGER.warning('Image conversion failed for attachment_id %s - %s',
                               self.attachment_id, self.path)

                # catch normal/expected errors and log them
                log_error('image_conversion')

        def delete_temp_file():
            """
            deletes the tempfile where the s3 object was downloaded to and it's reference
            """

            LOGGER.debug('Received call to delete_temp_file for attachment_id %s - %s',
                         self.attachment_id, self.path)

            os.remove(self.path)

            del self.path

        def export_pages():
            """
            save pages as images to the image store directory
            """

            LOGGER.debug('Received call to export_pages for attachment_id %s',
                         self.attachment_id)

            # create the image folder path and empty list for filepaths
            f = '%s/%s' % (local_config.image_store_dir, self.attachment_id)
            self.image_folder = f
            self.image_filepaths = []

            # try to create the folder, carry on if folder already exists
            try:

                os.mkdir(f)
                LOGGER.debug('New folder created %s', f)

            except FileExistsError:

                LOGGER.warning('Folder already exists %s', f)

            # save each page
            for i in range(len(self.pages)):

                # make filename
                fn = f + '/' + str(self.attachment_id) + '_' + str(i + 1) + '.png'

                # try to save the image to above path
                try:

                    LOGGER.debug('Exporting %s', fn)
                    Image.fromarray(self.pages[i]).save(fn)
                    self.image_filepaths.append(fn)

                # if there's an error as it as an erro
                except Exception as e:

                    LOGGER.warning('Export of %s failed - %s', fn, e)
                    log_error('image_export')

        def process_file():
            """
            download file from S3 to temp and convert to image
            """

            LOGGER.debug('Received call to process_file for attachment_id %s',
                         self.attachment_id)

            # create a temporary file to download to
            f = tempfile.NamedTemporaryFile(delete=False)

            # try to download the s3 object to the temporary file
            try:

                self.s3_object.download_fileobj(f)
                self.path = f.name
                self.mime_type = check_mime_type()[0]

            # if we encounter an error log it
            except ClientError as e:

                LOGGER.warning('Failed to download attachment_id %s - %s',
                               self.attachment_id, self.s3_object.key)
                log_error('download')

            # if we've got a file path then attempt to convert to images and export
            if hasattr(self, 'path'):
                process_pdf_to_image()
                export_pages()

            # if we didn't pick up any errors then can delete the file
            if not self.errored:
                delete_temp_file()

        def extract_uids_from_attachment_path():
            """
            extract the patient and referral uids from filename
            """

            LOGGER.debug('Received call to extract_uids_from_attachment_path\
                         for attachment_id %s', self.attachment_id)

            # patient_uid and referral_uid split by an underscore
            s = self.s3_object.key.split('_')
            self.tk_db_attachment.patient_uid = s[0]
            self.tk_db_attachment.referral_uid = s[1]

        # create the attributes
        self.errors = []
        self.errored = False
        self.gr_attachment = gr_attachment
        self.s3_object = create_s3_object()
        self.tk_db_attachment = add_to_db()
        self.attachment_id = self.tk_db_attachment.attachment_id
        self.pages = []
        self.person_name = None
        self.dob = None

        # do processing of file - download, convert to image, export
        process_file()

        # match to patient and referral
        extract_uids_from_attachment_path()

    def add_pages_to_db(self):
        """
        add relevant rows to page table of database
        """

        for i in range(len(self.pages)):
            self.tk_db_attachment.images.append(tk_db.Page(
                path=self.image_filepaths[i],
                page_number=i + 1,
                page_empty=self.empty_pages[i]
            ))

    def get_patient_info(self, session):
        """
        get patient info from GR database for the form's owner
        """

        LOGGER.debug('Received call to get_patient_info for attachment_id %s; patient_uid %s',
                     self.attachment_id, self.tk_db_attachment.patient_uid)

        q = session.query(gr_db.Person.person_first_name,
                          gr_db.Person.person_family_name,
                          gr_db.Patient.patient_date_of_birth).\
            join(gr_db.Person,
                 gr_db.Person.uid == gr_db.Patient.person_uid).\
            filter(gr_db.Patient.uid == self.tk_db_attachment.patient_uid).\
            first()

        # if we've got values for fore and surname and dob, then process
        if all(x is not None for x in q):
            self.person_name = f'{q[0]} {q[1]}'.upper()
            self.dob = '{0:%Y-%m-%d}'.format(q[2])

        else:

            LOGGER.warning('Unable to link %s to valid participant', self.attachment_id)
            self.errors.append('linking to participant')

    def crop_page(self, p, x, y, w, h, fw):
        """
        crop out a specific portion of a page, and return it to specific width
        and height
        if x + w or y + h > 1 then just crops to limit of image
        :params p: page number
        :params x: top left corner to start crop as proportion of page width
        :params y: top left corner to start crop as proportion of page width
        :params w: proportion of page width to include in crop
        :params h: proportion of page height to include in crop
        :params fw: final width of image in pixels to crop to
        :returns: crop of page to required limits
        """

        assert( 1 <= p <= len(self.pages),
               'page number requested outside of range for attachment')
        assert(all([0 <= x <= 1 for x in [x, y, w, h]]),
               'x, y, w, and h must all be in 0-1 range')

        LOGGER.debug('Received call to crop_page for attachment_id %s',
                     self.attachment_id)

        # get image sizes and resize factors
        img = self.pages[p - 1]
        ih, iw = img.shape
        f = iw / fw

        # crop out the relevant part of the image
        cimg = img[int(ih * y):int(ih * min(y + h, 1)),
                   int(iw * x):int(iw * min(x + w, 1))]

        # return a resized version of the crop
        return cv2.resize(cimg, dsize=(int(ih / f), fw))

    # GOT TO HERE
    def create_fault_ticket_url(self):
        """
        create url for creating a JIRA ticket, used as a link in the
        inspection ticket
        :returns: url string
        """

        # dictionary of key:value pairs for the resulting ticket
        d = {
            "reporter": "sthompson",
            "issuetype": "3",
            "assignee": "sthompson",
            "summary": 'Consent Form Fault for File %s' % self.attachment_id,
            "description": "Something has gone wrong with this file.\n Original location %s/%s" % (self.s3_object.bucket_name, self.s3_object.key),
            "pid": "11438"
        }

        # make the url
        url = '%s/secure/CreateIssueDetails!init.jspa?%s' % (
            local_config.jira_config['url'], urllib.parse.urlencode(d))

        return url

    def __repr__(self):
        return('<Attachment - ID %s>' % self.attachment_id)
