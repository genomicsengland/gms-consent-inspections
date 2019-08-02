#!/usr/bin/env python3
#Scripts to help do the manual inspection of GMS consent forms
import fire
import logging
import log
import subprocess
import local_config
from sqlalchemy.orm import sessionmaker
from modules import s3, pdf_file
from models import getEngine, makeSession, gms_consent_db

logger = logging.getLogger(__name__)

def autoModelGen(db_conn_str, schema, outfile):
    """Automatically generate sqlalchemy model from existing db"""
    logger.info("Running autoModelGen with arguments: %s > %s > %s" % (db_conn_str, schema, outfile))
    subprocess.call(["sqlacodegen", db_conn_str,
                     "--schema", schema,
                     "--outfile", outfile])

# create class that will become command argument with Fire
# e.g. python3 ngis_mq.py RunReferralTests
class ConsInsp(object):

    def generateGRModel(self, fn = 'models/gr_db.py'):
        """generate the gr_db model"""
        logger.info("Running GenerateGRModel")
        autoModelGen(local_config.gr_db_connection_string,
                     'public',
                     fn)

    def dlFile(self):
        s = s3.ConnectToS3()
        with open('test.pdf', 'wb') as f:
            s.download_fileobj('formLibrary', 'Consent.pdf#test1', f)

    def listFiles(self):
        l = s3.listBucketFiles('patient-records')
        s = makeSession()
        for i in l:
            #logger.info('Processing %s' % i.key)
            c = pdf_file.ConsentForm(i, 'id')
            c.addToDB(s)
        s.commit()

    def getAFile(self):
        s = makeSession()
        l = s3.listBucketFiles('patient-records')
        o = [s3.createS3Obj(b, k) for b, k in l]
        c = pdf_file.ConsentForm(o[100], 'id3')
        c.exportPages('/Users/simonthompson/scratch')
        print(c.image_filepaths)
        c.addToDB(s)
        s.commit()

    def recreateConsentDB(self):
        logger.info('Running recreateConsentDB')
        e = getEngine(local_config.gms_consent_db_connection_string)
        gms_consent_db.metadata.drop_all(e)
        gms_consent_db.metadata.create_all(e)

if __name__ == "__main__":
    fire.Fire(ConsInsp)

