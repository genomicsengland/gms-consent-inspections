# provides two different JIRA Ticket classes
import requests
import logging
from local_config import jira_config
import io
from PIL import Image
import datetime
import sys

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
        attachments - a list to accommodate tuples of (attachment name, numpy array) attachments to be uploaded
        issuetype - the type of ticket (task, bug etc.)
        summary - the title of the ticket
        description - the main text of the ticket
    """

    project = 'CDT'
    assignee = 'sthompson'
    attachments = []
    issuetype = 'Task'
    ticket_id = None
    summary = 'Default summary'
    description = 'Default description'

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
        self.ticket_id = createJiraIssue(d)
        logger.info('Ticket %s created - %s/browse/%s' % (self.ticket_id, jira_config['url'], self.ticket_id))
        # upload the attachments
        if len(self.attachments):
            for i in self.attachments:
                uploadAttachment(self.ticket_id, i[0], i[1])
            logger.info('%s attachments added' % len(self.attachments))

class InspectionTicket(Ticket):
    """
    An inspection ticket inheriting from the Ticket class

    Extra attributes:
        description_table: empty list to accommodate the list of lists that will be reformatted into a JIRA table by parseTableToDescription
    """

    def __init__(self, description_table):

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
        self.description = parseTableToDescription(description_table)
        self.summary = 'GMS Consent Inspection %s' % '{0:%Y-%m-%d}'.format(datetime.datetime.today())


class ErrorTicket(Ticket):
    """a type of ticket to record errors associated with getting files"""

    def __init__(self, e, file_id):
        logger.debug("Creating new instance of ErrorTicket")
        self.summary = 'Consent Error for file id %s' % file_id
        self.description = 'There was an %s issue with this file' % e

