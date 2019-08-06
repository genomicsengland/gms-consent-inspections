# provides functionality around jira ticket creation
import requests
import logging
from local_config import jira_config
import io
from PIL import Image

logger = logging.getLogger(__name__)

# set up session
try:
    logger.debug("Setting up JIRA connection")
    s = requests.Session()
    s.auth = (jira_config['user'], jira_config['password'])
except requests.exceptions.RequestException as e:
    logger.critical("Unable to establish session with Confluence - %s" % e)
    sys.exit(1)

def createJiraIssue(d):
    """create a new jira issue using the content given"""
    logger.debug('Received call to createJiraIssue')
    url = jira_config['url'] + '/rest/api/2/issue/'
    try:
        r = s.post(url, json = d)
        r.raise_for_status()
        logger.info('Created %s' % r.json()['key'])
    except requests.exceptions.RequestException as e:
        logger.debug('Failed to create issue - e' % e)
        #sys.exit(1) comment out for debugging
    return r.json()['key']

def uploadAttachment(k, n, i):
    """Upload a numpy array (i) to a jira ticket (k) as a png with name n"""
    url = jira_config['url'] + '/rest/api/2/issue/' + k + '/attachments'
    try:
        r = s.post(url, files = {'file' : (n, arrayToBytes(i))}, headers = {"X-Atlassian-Token": "nocheck"})
        r.raise_for_status
    except requests.exceptions.RequestException as e:
        logger.debug('Failed to upload image - %s' % e)
        #sys.exit(1) comment out for debugging

def arrayToBytes(arr):
    """convert numpy array to a bytes object for upload"""
    b = io.BytesIO()
    i = Image.fromarray(arr).save(b, format='PNG')
    b = b.getvalue()
    return b
