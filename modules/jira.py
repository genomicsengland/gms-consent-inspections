# provides two different JIRA Ticket classes
import requests
import logging
from local_config import jira_config
import io
from PIL import Image
import datetime
import sys
from models import tk_db

logger = logging.getLogger(__name__)

# set up a requests session for talking to JIRA
try:
    logger.debug("Setting up JIRA connection")
    s = requests.Session()
    s.auth = (jira_config['user'], jira_config['password'])
except requests.exceptions.RequestException as e:
    logger.critical("Unable to establish session with JIRA - %s" % e)
    sys.exit(1)

def createJiraIssue(d):
    """REST API call to create a new jira issue using the content given"""
    url = jira_config['url'] + '/rest/api/2/issue'
    logger.debug('Received call to createJiraIssue - %s' % url)
    try:
        r = s.post(url, json = d)
        r.raise_for_status()
        return r.json()['key']
    except requests.exceptions.RequestException as e:
        logger.debug('Failed to create issue - e')
        sys.exit(1)

def uploadAttachment(k, n, i):
    """Upload a numpy array (i) to a jira ticket (k) as a png with name n"""
    url = jira_config['url'] + '/rest/api/2/issue/' + k + '/attachments'
    try:
        r = s.post(url, files = {'file' : (n, arrayToBytes(i))}, headers = {"X-Atlassian-Token": "nocheck"})
        r.raise_for_status
    except requests.exceptions.RequestException as e:
        logger.debug('Failed to upload image - %s' % e)
        sys.exit(1)

def arrayToBytes(arr):
    """convert numpy array to a bytes object for upload"""
    b = io.BytesIO()
    i = Image.fromarray(arr).save(b, format='PNG')
    b = b.getvalue()
    return b

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
        logger.debug('Creating new instance of Ticket')

    def createTicket(self):
        """generate the JSON object to be pushed to the REST API and create the ticket"""
        logger.debug('Received call to createTicket')
        # gather together data for creating the ticket
        d = {
            "fields" : {
            'project' : {'key' : self.project},
            'summary' : self.summary,
            'description' : self.description,
            'issuetype' : {'name' : self.issuetype},
            'assignee' : {'name' : self.assignee}
            }}
        # create the ticket
        self.ticket_key = createJiraIssue(d)
        # update the SQLachmemy object with the ticket key
        self.tracking_db_ticket.ticket_key = self.ticket_key
        logger.info('Ticket %s created - %s/browse/%s' % (self.ticket_key, jira_config['url'], self.ticket_key))
        # upload the attachments
        if len(self.ticket_image_attachments):
            for i in self.ticket_image_attachments:
                uploadAttachment(self.ticket_key, i[0], i[1])
            logger.info('%s attachments added' % len(self.ticket_image_attachments))



class InspectionTicket(Ticket):
    """
    An inspection ticket inheriting from the Ticket class

    Extra attributes:
        description_table: empty list to accommodate the list of lists that will be reformatted into a JIRA table by parseTableToDescription
        tracking_db_ticket: instance of tk_db.Ticket
    """

    def __init__(self, session, description_table, attachment_objects):
        """set up a new instance of InspectionTicket class
        
        Arguments:
            session: a SQLAlchemy session
            description_table: a list of lists that represent a table to be placed in ticket description
            attachment_objects: list of instances of attachment.Attachment"""

        def parseTableToDescription(t):
            """convert list of lists to a jira markup table and update ticket description"""
            logger.debug('Received call to parseTable')
            out = []
            for i in range(len(t)):
                if i == 0:
                    out.append('||' + '||'.join(t[i]) + '||')
                else:
                    out.append('|' + '|'.join(t[i]) + '|')
            return '\n'.join(out)

        logger.debug('Creating new instance of InspectionTicket')
        # create the description table
        self.description = parseTableToDescription(description_table)
        # populate the summary field
        self.summary = 'GMS Consent Inspection %s' % '{0:%Y-%m-%d}'.format(datetime.datetime.today())
        # create a new instance of tk_db.Ticket
        self.tracking_db_ticket = tk_db.Ticket(ticket_key = 'UNK', ticket_assignee = self.assignee, ticket_status = 'new')
        # add in the Attachment.index_attachment for each of the attachments featured in the ticket
        self.tracking_db_ticket.attachment = [x.index_attachment for x in attachment_objects]
        # add the object into the session
        session.add(self.tracking_db_ticket)
        session.flush()
        # update the ticket_id
        self.ticket_id = self.tracking_db_ticket.ticket_id

class ErrorTicket(Ticket):
    """An error ticket inheriting from the Ticket class"""

    def __init__(self, session, attachment_object):
        """initiate a new instance of Error Ticket
        
        Arguments:
            session: a SQLalchemy session
            attachment_object: an instance of attachment.Attachment
            """

        logger.debug("Creating new instance of ErrorTicket")
        # populate the text fields
        self.summary = 'Consent Error for file id %s' % attachment_object.attachment_id
        self.description = 'There was an %s issue with this file' % ';'.join(attachment_object.errors) 
        # create a new instance of tk_db.Ticket
        self.tracking_db_ticket = tk_db.Ticket(ticket_key = 'UNK', ticket_assignee = self.assignee, ticket_status = 'error')
        # add in reference for the Attachment.index_attachment
        self.tracking_db_ticket.errors = [tk_db.Error(attachment_error = attachment_object.index_attachment)]
        # add the object to the session
        session.add(self.tracking_db_ticket)
        session.flush()
        # update the ticket_id
        self.ticket_id = self.tracking_db_ticket.ticket_id

