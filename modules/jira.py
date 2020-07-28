"""
provides two different JIRA Ticket Classes built off the parent
Ticket class
"""
# provides two different JIRA Ticket classes
import logging
import sys
import datetime
import io
import requests
from PIL import Image
from local_config import jira_config
from models import tk_db


LOGGER = logging.getLogger(__name__)


# set up a requests session for talking to JIRA
try:
    LOGGER.debug("Setting up JIRA connection")
    s = requests.Session()
    s.auth = (jira_config['user'], jira_config['password'])
except requests.exceptions.RequestException as e:
    LOGGER.critical("Unable to establish session with JIRA - %s" % e)
    sys.exit(1)


def create_jira_issue(d):
    """
    REST API call to create a new jira issue using the content given
    :params d: dictionary of data to send to make the ticket
    :returns: ticket key of created ticket
    """

    # make the url to send the request to
    url = jira_config['url'] + '/rest/api/2/issue'

    LOGGER.debug('Received call to create_jira_issue - %s', url)

    # try to post and create the ticket
    try:
        r = s.post(url, json=d)
        r.raise_for_status()
        return r.json()['key']

    # if this doesn't work, exit
    except requests.exceptions.RequestException as e:
        LOGGER.debug('Failed to create issue - e')
        sys.exit(1)


def upload_attachment(k, n, i):
    """
    Upload a numpy array to a jira ticket as a png
    :params k: JIRA ticket key
    :params n: filename for image to be uploaded as, should end with .png
    :params i: Numpy array of the image
    """

    # make the url to send the request to
    url = jira_config['url'] + '/rest/api/2/issue/' + k + '/attachments'

    # try to post the request, including conversion of the Numpy array to a
    # Bytes object
    try:
        r = s.post(url, files={
            'file': (n, array_to_png(i))
        }, headers={"X-Atlassian-Token": "nocheck"})
        r.raise_for_status

    # if this doesn't work, exit
    except requests.exceptions.RequestException as e:
        LOGGER.debug('Failed to upload image - %s', e)
        sys.exit(1)


def array_to_png(arr):
    """
    convert numpy array to a PNG bytes object for upload
    :params arr: Numpy array
    :returns: Bytes object with PNG format
    """

    # create the Bytes object
    b = io.BytesIO()

    # fill it with the Image generated from the array
    Image.fromarray(arr).save(b, format='PNG')

    # return the Bytes value
    return b.getvalue()


class Ticket:
    """
    Base class for the different JIRA ticket types

    Attributes:
        project - the name of the JIRA project where the tickets will end up
        assignee - the username of the person who the tickets will be assigned to
        ticket_image_attachments - a list to accommodate tuples of (attachment name, numpy array) of image attachments to be uploaded
        issuetype - the type of ticket (task, bug etc.)
        summary - the title of the ticket
        description - the main text of the ticket
        ticket_key - the name of the ticket
        ticket_id - the id of the ticket in the Index db
    """

    project = 'CDT'
    assignee = 'sthompson'
    ticket_image_attachments = []
    issuetype = 'Task'
    ticket_key = None
    summary = 'Default summary'
    description = 'Default description'
    ticket_id = None

    def __init__(self):

        LOGGER.debug('Creating new instance of Ticket')

    def create_ticket(self):
        """
        generate the JSON object to be pushed to the REST API and create the ticket
        """

        LOGGER.debug('Received call to create_ticket')

        # gather together data for creating the ticket
        d = {
            "fields": {
                'project': {'key': self.project},
                'summary': self.summary,
                'description': self.description,
                'issuetype': {'name': self.issuetype},
                'assignee': {'name': self.assignee}
            }}

        # create the ticket
        self.ticket_key = create_jira_issue(d)

        # update the SQLachmemy object with the ticket key
        self.tracking_db_ticket.ticket_key = self.ticket_key

        LOGGER.info('Ticket %s created - %s/browse/%s',
                    self.ticket_key, jira_config['url'], self.ticket_key)

        # if there are any attachments added to the ticket
        if len(self.ticket_image_attachments):
            # upload each one
            for i in self.ticket_image_attachments:
                upload_attachment(self.ticket_key, i[0], i[1])

            LOGGER.info('%s attachments added',
                        len(self.ticket_image_attachments))


class InspectionTicket(Ticket):
    """
    An inspection ticket inheriting from the Ticket class

    Extra attributes:
        description_table: empty list to accommodate the list of lists that
        will be reformatted into a JIRA table by parseTableToDescription
        tracking_db_ticket: instance of tk_db.Ticket
    """

    def __init__(self, session, description_table, attachment_objects):
        """
        create a new instance of InspectionTicket
        :params session: a SQLAlchemy session
        :params description_table: a list of lists that represent a table to be
        placed in ticket description
        :params attachment_objects: list of instances of attachment.Attachment
        """

        def format_table(t):
            """
            convert list of lists to a jira markup table and update ticket
            description
            :params t: list of lists with each element being a row
            :returns: string with linebreaks
            """

            LOGGER.debug('Received call to parseTable')

            out = []

            # process each row
            for i in range(len(t)):

                # if it's the header we need to separate by double pipe
                if i == 0:
                    out.append('||' + '||'.join(t[i]) + '||')

                # otherwise we just single pipe separate
                else:
                    out.append('|' + '|'.join(t[i]) + '|')

            # return the full string separated by line breaks
            return '\n'.join(out)

        LOGGER.debug('Creating new instance of InspectionTicket')

        # create the description table
        self.description = format_table(description_table)

        # populate the summary field
        self.summary = 'GMS Consent Inspection %s' % '{0:%Y-%m-%d}'.\
            format(datetime.datetime.today())

        # create a new instance of tk_db.Ticket
        self.tracking_db_ticket = tk_db.Ticket(
            ticket_assignee=self.assignee, ticket_status='new')

        # add in the Attachment.index_attachment for each of the attachments
        # featured in the ticket
        self.tracking_db_ticket.attachment = [
            x.index_attachment for x in attachment_objects]

        # add the object into the session
        session.add(self.tracking_db_ticket)
        session.flush()

        # update the ticket_id
        self.ticket_id = self.tracking_db_ticket.ticket_id


class ErrorTicket(Ticket):
    """
    An error ticket inheriting from the Ticket class
    """

    def __init__(self, session, attachment_object):
        """
        initiate a new instance of Error Ticket
        :params session: a SQLalchemy session
        :params attachment_object: an instance of attachment.Attachment
        """

        LOGGER.debug("Creating new instance of ErrorTicket")

        # populate the text fields
        self.summary = 'Consent Error for file id %s' %\
            attachment_object.attachment_id
        self.description = 'There was an %s issue with this file' %\
            ';'.join(attachment_object.errors)

        # create a new instance of tk_db.Ticket
        self.tracking_db_ticket = tk_db.Ticket(ticket_assignee=self.assignee,
                                               ticket_status='error')

        # add in reference for the Attachment.index_attachment
        self.tracking_db_ticket.errors = [
            tk_db.Error(attachment_error=attachment_object.index_attachment)]

        # add the object to the session
        session.add(self.tracking_db_ticket)
        session.flush()

        # update the ticket_id
        self.ticket_id = self.tracking_db_ticket.ticket_id
