from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from models import gms_consent_db, gr_db
from local_config import gms_consent_db_connection_string, gr_db_connection_string

logger = logging.getLogger(__name__)

def makeSession():
    """get session for all bound dbs"""
    logger.info('Received call to makeSession')
    session = sessionmaker()
    session.configure(binds = {
        gms_consent_db.Base : getEngine(gms_consent_db_connection_string),
        gr_db.Base : getEngine(gr_db_connection_string)
    })
    return session()

def getEngine(conn):
    """get an engine for the given connection string"""
    logger.debug('Received call to getEngine for %s' % conn)
    return create_engine(conn, echo = False)
