#!/usr/bin/env python3
#Scripts to help do the manual inspection of GMS consent forms
import fire
import logging
import log
import subprocess
import local_config
from sqlalchemy.orm import sessionmaker
from modules import s3, pdf_file

logger = logging.getLogger(__name__)

def makeSession():
    """get session object and bind different engines to the different declarative bases for each db"""
    logger.info("Making db session")
    session = sessionmaker()
    session.configure(binds = {gr_db.Base:GetEngine(local_config.gr_db_connection_string),
                            config_db.Base:GetEngine(local_config.config_db_connection_string),
                               res_db.Base:GetEngine(local_config.res_db_connection_string)})
    return session()

def autoModelGen(db_conn_str, schema, outfile):
    """Automatically generate sqlalchemy model from existing db"""
    logger.info("Running autoModelGen with arguments: %s > %s > %s" % (db_conn_str, schema, outfile))
    subprocess.call(["sqlacodegen", db_conn_str,
                     "--schema", schema,
                     "--outfile", outfile])

# create class that will become command argument with Fire
# e.g. python3 ngis_mq.py RunReferralTests
class ConsInsp(object):

    def GenerateGRModel(self, fn = 'models/gr_db.py'):
        """generate the gr_db model"""
        logger.info("Running GenerateGRModel")
        autoModelGen(local_config.gr_db_connection_string,
                     'public',
                     fn)

    def DlFile(self):
        s = s3.ConnectToS3()
        with open('test.pdf', 'wb') as f:
            s.download_fileobj('formLibrary', 'Consent.pdf#test1', f)

    def ListFiles(self):
        l = s3.listBucketFiles('patient-records')
        print(l[0:100])

    def GetAFile(self):
        l = s3.listBucketFiles('patient-records')
        o = [s3.createS3Obj(b, k) for b, k in l]
        c = pdf_file.ConsentForm(o[100], 'id3')
        c.ExportPages('/Users/simonthompson/scratch')
        print(c.image_filepaths)

if __name__ == "__main__":
    fire.Fire(ConsInsp)

