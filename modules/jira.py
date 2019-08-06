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
    """create a new jira issue using the content given"""
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

class InspectionTicket:
    """an inspection ticket instance"""

    def __init__(self):
        logger.debug('Creating new instance of InspectionTicket')
        self.summary = 'Consent Inspection %s' % '{0:%Y-%m-%d}'.format(datetime.datetime.today())
        self.project = 'CDT'
        self.issuetype = 'Task'
        self.assignee = 'sthompson'
        self.description = "If you're seeing this, we're in trouble - CALL THE WRANGLERS!!!"
        # empty list to accommodate tuples of attachment name, numpy array of image crop to be uploaded
        self.attachments = []
        # empty list to accommodate list of lists that represent the table for description
        self.description_table = []
        self.ticket_id = None

    def parseTable(self):
        """convert list of lists to a jira markup table"""
        logger.debug('Received call to parseTable')
        out = []
        for i in range(len(self.description_table)):
            if i == 0:
                out.append('||' + '||'.join(self.description_table[i]) + '||')
            else:
                out.append('|' + '|'.join(self.description_table[i]) + '|')
        return '\n'.join(out)

    def createTicket(self):
        """generate the actual ticket"""
        logger.debug('Received call to createTicket')
        # gather together data for creating the ticket
        self.description = self.parseTable()
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
        logger.info('Inspection ticket %s created' % self.ticket_id)
        # upload the attachments
        for i in self.attachments:
            uploadAttachment(self.ticket_id, i[0], i[1])
        logger.info('%s attachments added' % len(self.attachments))

class ErrorTicket:
    """a type of ticket to record errors associated with getting files"""

    def __init__(self, e, file_id):
        logger.debug("Creating new instance of ErrorTicket")
        self.summary = 'Consent Error for file id %s' % file_id
        self.project = 'CDT'
        self.issuetype = 'Task'
        self.assignee = 'sthompson'
        self.description = 'There was an %s issue with this file' % e
        self.ticket_id = None

    def createTicket(self):
        """generate the actual ticket"""
        logger.debug('Received call to createTicket')
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
        logger.info('Error ticket %s created' % self.ticket_id)


