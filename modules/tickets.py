# provides class and functions for finding existing and new tickets
import requests
import logging
from local_config import jira_config
import datetime
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

def getTicket(k):
    """make a call to JIRA REST API to get ticket (k) details."""
    logger.debug('Received call to getTicket for %s' % k)
    url = '%s/rest/api/2/issue/%s' % (jira_config['url'], k)
    try:
        r = s.get(url)
        r.raise_for_status()
        logger.debug('Made call to %s' % url)
        return r.json()['fields']
    except requests.exceptions.HTTPError as e:
        logger.info('Ticket %s not found' % k)

def listJiraIssues(jql):
    """Return all Jira issues fitting a query, iterating over required number of pages"""
    logger.debug('Received call to listJiraIssues function - %s' % jql)
    npp = 100
    r = getJiraIssuesPage(jql, st = 0, npp = npp)
    out = r['issues']
    nr = r['total']
    start = r['startAt']
    while len(out) != nr:
        r = getJiraIssuesPage(jql, st = start + npp, npp=npp)
        start = r['startAt']
        out = out + r['issues']
    logger.info('%s records read from JIRA' % (str(len(out))))
    return [x['key'] for x in out]

def getJiraIssuesPage(jql, st, npp):
    """Returns a single page of jrl query for given start and number of records"""
    url = '%s/rest/api/2/search?jql=%s&startAt=%s&maxResults=%s' % (jira_config['url'], jql, st, npp)
    logger.debug('Received call to getJiraIssuesPage function - %s' % url)
    try:
        r = s.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        logger.critical("Unable to get page from JIRA - %s" % e)
        sys.exit(1)

class ExistingTicket:
    """An existing JIRA ticket that was previously created and exists in db
    
    Attributes:
        tracker_db_ticket: instance of tk_db.Ticket
        key: the key of the JIRA ticket
        status: the current status of the JIRA ticket
        assignee: the current assignee of the JIRA ticket
    """

    def __init__(self, tracker_db_ticket):
        """Initiate a new instance of Existing Ticket"""
        logger.debug('Making new instance of ExistingTicket')
        self.tracker_db_ticket = tracker_db_ticket
        self.key = tracker_db_ticket.ticket_key
        # get the ticket details from JIRA
        d = getTicket(self.key)
        # if ticket exists then update attributes
        if d is not None:
            logger.debug('Ticket found, updating attributes')
            self.status = d['status']['name']
            self.assignee = d['assignee']['name']
        # if request was unsuccessfull then update attributes
        else:
            logger.debug('Ticket not found, updating attributes')
            self.status = 'not found'
            self.assignee = None

    def updateDB(self):
        """Function to update the tk_db.Ticket instance"""
        logger.debug('Received call to updateDB')
        self.tracker_db_ticket.ticket_status = self.status
        self.tracker_db_ticket.ticket_assignee = self.assignee
        self.tracker_db_ticket.ticket_updated = datetime.datetime.today()

class NewTicket:
    """A JIRA ticket that doesn't currently exist in db (created during consent check)
    
    Attributes:
        key: the key of the JIRA ticket
        attachment_id: the ID of the attachment the ticket concerns
        status: the current status of the JIRA ticket
        assignee: the current assignee of the JIRA ticket
        tracker_db_ticket: instance of tk_db.Ticket
    """

    def __init__(self, key):
        """Initiate a new instance of NewTicket with JIRA ticket key"""
        logger.debug('Making new instance of NewTicket for %s' % key)
        self.key = key
        # get ticket details
        d = getTicket(self.key)
        # split title to get attachment ID
        l = d['summary'].split(' File ')
        # make attributes
        self.attachment_id = l[1]
        self.status = d['status']['name']
        self.assignee = d['assignee']['name']
        # make instance of tk_db.Ticket
        self.tracker_db_ticket = tk_db.Ticket(ticket_key = self.key)
        logger.info('Got new ticket - %s - for attachment_id %s' % (self.key, self.attachment_id))

    def updateDB(self, session, error_type):
        """Function to update the tk_db with new objects which will be added to
        session and given the error_type argument"""
        # get the tk_db.Attachment object for attachment_id
        att = session.query(tk_db.Attachment).\
            filter(tk_db.Attachment.attachment_id == self.attachment_id).first()
        # add the tk_db.Ticket instance to session
        session.add(self.tracker_db_ticket)
        # make new tk_db.Error instance, linking to the attachment and ticket
        err = tk_db.Error(error_type = error_type)
        err.attachment_error = att
        err.ticket_error = self.tracker_db_ticket
        # add it to the session
        session.add(err)
        # update the tk_db.Ticket attributes
        self.tracker_db_ticket.ticket_status = self.status
        self.tracker_db_ticket.ticket_assignee = self.assignee
        self.tracker_db_ticket.ticket_updated = datetime.datetime.today()



