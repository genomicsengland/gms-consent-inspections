"""
provides functions for working with JIRA tickets
also provides two classes for instances of JIRA tickets that
either exist in the database already or are unknown to it
"""
import requests
import datetime
import sys
import logging
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


def get_ticket(k):
    """
    make a call to JIRA REST API to get ticket details
    :params k: ticket key
    :returns: dictionary of ticket fields
    """

    LOGGER.debug('Received call to get_ticket for %s', k)

    # make request url
    url = '%s/rest/api/2/issue/%s' % (jira_config['url'], k)

    # get ticket details
    r = s.get(url)
    r.raise_for_status()

    LOGGER.debug('Made call to %s', url)

    return r.json()['fields']


def list_jira_issues(jql):
    """
    Return all Jira issues matching a query, iterating over required number of
    pages
    :params jql: string of jira query language for issues to return
    :returns: list of ticket keys matching query
    """

    LOGGER.debug('Received call to listJiraIssues function - %s' % jql)

    # asking for 100 issues per page
    npp = 100

    # get the first page of matches
    r = get_jira_issues_page(jql, st=0, npp=npp)

    # add the issues to a list and get number of total tickets in query
    # and where we started at to get the next page
    out = r['issues']
    nr = r['total']
    start = r['startAt']

    # if there are still tickets to get, go get them
    while len(out) != nr:

        # make the call for the next page
        r = get_jira_issues_page(jql, st=start + npp, npp=npp)

        # update the variables
        start = r['startAt']
        out = out + r['issues']

    LOGGER.info('%s records read from JIRA', len(out))

    return [x['key'] for x in out]


def get_jira_issues_page(jql, st, npp):
    """
    Returns a single page of jql query matches
    :params jql: jira query language string
    :params st: start number of page
    :params npp: number of issues per page to return
    """

    # create the request url
    url = '%s/rest/api/2/search?jql=%s&startAt=%s&maxResults=%s' %\
        (jira_config['url'], jql, st, npp)

    LOGGER.debug('Received call to getJiraIssuesPage function - %s' % url)

    try:
        r = s.get(url)
        r.raise_for_status()
        return r.json()

    except requests.exceptions.RequestException as e:
        LOGGER.critical("Unable to get page from JIRA - %s" % e)
        sys.exit(1)


class ExistingTicket:
    """
    An existing JIRA ticket that was previously created and exists in db
    
    Attributes:
        tracker_db_ticket: instance of tk_db.Ticket
        key: the key of the JIRA ticket
        status: the current status of the JIRA ticket
        assignee: the current assignee of the JIRA ticket
    """

    def __init__(self, tracker_db_ticket):
        """
        Initiate a new instance of Existing Ticket
        :params tracker_db_ticket: SQLAlchemy object corresponding to the
        ticket in the database
        """

        LOGGER.debug('Making new instance of ExistingTicket')

        self.tracker_db_ticket = tracker_db_ticket
        self.key = tracker_db_ticket.ticket_key

        # get the ticket details from JIRA
        d = get_ticket(self.key)

        # if ticket exists then update attributes
        if d is not None:

            LOGGER.debug('Ticket found, updating attributes')

            self.status = d['status']['name']
            self.assignee = d['assignee']['name']

        # if request was unsuccessfull then update attributes
        else:

            LOGGER.debug('Ticket not found, updating attributes')

            self.status = 'not found'
            self.assignee = None


    def update_db(self):
        """
        update the database with the ticket details
        """

        LOGGER.debug('Received call to updateDB')

        self.tracker_db_ticket.ticket_status = self.status
        self.tracker_db_ticket.ticket_assignee = self.assignee
        self.tracker_db_ticket.ticket_updated = datetime.datetime.today()


class NewTicket:
    """
    A JIRA ticket that doesn't currently exist in db (created during consent
    inspection)
    
    Attributes:
        key: the key of the JIRA ticket
        attachment_id: the ID of the attachment the ticket concerns
        status: the current status of the JIRA ticket
        assignee: the current assignee of the JIRA ticket
        tracker_db_ticket: instance of tk_db.Ticket
    """

    def __init__(self, key):
        """
        Initiate a new instance of NewTicket with JIRA ticket key
        """

        LOGGER.debug('Making new instance of NewTicket for %s' % key)

        self.key = key

        # get ticket details
        d = get_ticket(self.key)

        # split title to get attachment ID
        l = d['summary'].split(' File ')

        # make attributes
        self.attachment_id = l[1]
        self.status = d['status']['name']
        self.assignee = d['assignee']['name']

        # make instance of tk_db.Ticket
        self.tracker_db_ticket = tk_db.Ticket(ticket_key=self.key)

        LOGGER.info('Got new ticket - %s - for attachment_id %s',
                    self.key, self.attachment_id)


    def update_db(self, session, error_type):
        """
        update the database with the ticket details
        :params session: SQLAlchemy session boudn to required engines
        :params error_type: type of error in the ticket
        """

        LOGGER.debug('Updating database with ticket %s', self.key)

        # get the tk_db.Attachment object for attachment_id
        att = session.query(tk_db.Attachment).\
            filter(tk_db.Attachment.attachment_id == self.attachment_id).\
            first()

        # add the tk_db.Ticket instance to session
        session.add(self.tracker_db_ticket)

        # make new tk_db.Error instance, linking to the attachment and ticket
        err = tk_db.Error(error_type=error_type)
        err.attachment_error = att
        err.ticket_error = self.tracker_db_ticket

        # add it to the session
        session.add(err)

        # update the tk_db.Ticket attributes
        self.tracker_db_ticket.ticket_status = self.status
        self.tracker_db_ticket.ticket_assignee = self.assignee
        self.tracker_db_ticket.ticket_updated = datetime.datetime.today()
