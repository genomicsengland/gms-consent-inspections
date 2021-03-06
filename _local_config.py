# local configuration options
from string import Template
from modules import get_profile

##-- Connections
# psycopg2 connection string template
databaseStringTemplate = 'postgresql+psycopg2://$user:$password@$host:$port/$database'
conns = get_profile.get_profile(items = ['ngis_slave_db','s3_consent_keys', 'local_postgres_con', 'ldap'])

# S3 Bucket
s3_bucket_config = {**conns['s3_consent_keys'], 'url': 'https://cas.cor00005.ukcloud.com/'}

# GR Slave DB
gr_db_connection_string = Template(databaseStringTemplate).safe_substitute({**conns['ngis_slave_db'], "database": "ngis_genomicrecord_alpha"})

# Tracker DB
tk_db_connection_string = Template(databaseStringTemplate).safe_substitute({**conns['local_postgres_con'], "database": "testing"})

# JIRA connection
jira_config = {**conns['ldap'], 'url' : 'https://jira.extge.co.uk'}

# CIP-API connection
#cip_api_config = {**conns['cip_api'], 'url' : 'https://cipapi-gms-beta.gel.zone/'}

##-- File stores
# folder to put image exports of the consent form pages
image_store_dir = '/Users/simonthompson/scratch/temp'

##-- JIRA jsql strings
# JQL to get any consent form faults generated from consent form check tickets
consent_form_check_errors = 'project%20%3D%20"Clinical%20Data%20Wranglers%20%26%20Modellers"%20and%20summary%20~%20%27Consent%20Form%20Fault%27'
