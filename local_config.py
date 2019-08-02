# local configuration options
from string import Template
import get_profile

# psycopg2 connection string template
databaseStringTemplate = 'postgresql+psycopg2://$user:$password@$host:$port/$database'

conns = get_profile.getProfile(items = ['ngis_slave_db', 'mis_con', 's3_consent_keys', 'local_postgres_con'])

s3_bucket_config = {**conns['s3_consent_keys'], 'url': 'https://cas.cor00005.ukcloud.com/'}

# generate connection string to pass to SQLAlchemy Engine
gr_db_connection_string = Template(databaseStringTemplate).safe_substitute({**conns['ngis_slave_db'], "database": "ngis_genomicrecord_beta"})
gms_consent_db_connection_string = Template(databaseStringTemplate).safe_substitute({**conns['local_postgres_con'], "database": "testing"})

