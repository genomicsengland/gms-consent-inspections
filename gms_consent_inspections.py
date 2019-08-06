#!/usr/bin/env python3
#Scripts to help do the manual inspection of GMS consent forms
import fire
import logging
import log
import subprocess
import local_config
from sqlalchemy.orm import sessionmaker
from modules import s3, attachment, jira
from models import getEngine, makeSession, gms_consent_db, gr_db

logger = logging.getLogger(__name__)

def autoModelGen(db_conn_str, schema, outfile):
    """Automatically generate sqlalchemy model from existing db"""
    logger.info("Running autoModelGen with arguments: %s > %s > %s" % (db_conn_str, schema, outfile))
    subprocess.call(["sqlacodegen", db_conn_str,
                     "--schema", schema,
                     "--outfile", outfile])

def listToTable(l):
    """convert list of lists to jira style table"""
    out = []
    for i in range(len(l)):
        if i == 0:
            out.append('||' + '||'.join(l[i]) + '||')
        else:
            out.append('|' + '|'.join(l[i]) + '|')
    return '\n'.join(out)

defaultJiraIssueDict = {
"fields": {
    "project":
    {
        "key": "CDT"
    },
    "summary": "REST ye merry gentlemen.",
    "issuetype": {
        "name": "Bug"
    },
    "assignee":{
        "name":"sthompson"
    }
} }

# create class that will become command argument with Fire
# e.g. python3 ngis_mq.py RunReferralTests
class ConsInsp(object):

    def generateGRModel(self, fn = 'models/gr_db.py'):
        """generate the gr_db model"""
        logger.info("Running GenerateGRModel")
        autoModelGen(local_config.gr_db_connection_string,
                     'public',
                     fn)

    def process(self):
        s = makeSession()
        test_uids = s.query(gr_db.Attachment.uid, gr_db.Attachment.attachment_url).\
            filter(gr_db.Attachment.attachment_title == 'record-of-discussion-form.pdf')
        print(test_uids)
        objects = []
        table = [['id', 'name', 'dob', 'image', 'fault link']]
        crops = []
        for i in test_uids[0:3]:
            a = gms_consent_db.attachment(
                attachment_uid = i[0]
            )
            s.add(a)
            s.flush()
            b, k = i[1].split('/')
            o = s3.createS3Obj(b, k + 'jdfsk')
            c = attachment.Attachment(o, a)
            c.extractParticipantInfo(s)
            objects.append(c)
            if len(c.errors) == 0:
                table.append([str(c.attachment.file_id), c.person_name, c.dob, '!%s.png!' % c.attachment.file_id, '[Fault|%s]' % c.createFaultTicketURL()])
                crops.append(('%s.png' % c.attachment.file_id, c.cropImageArea(1, 0.5, 0.5, 0.25, 0.25, 150))) 
            else:
                t = jira.ErrorTicket(';'.join(c.errors), c.attachment.file_id)
                t.createTicket()
        t = jira.InspectionTicket()
        t.description_table = table
        t.attachments = crops
        t.createTicket()
        for i in objects:
            i.attachment.host_jira_ticket_id = t.ticket_id 
            i.addToDB(s)
        s.commit()

    def recreateConsentDB(self):
        logger.info('Running recreateConsentDB')
        e = getEngine(local_config.gms_consent_db_connection_string)
        gms_consent_db.metadata.drop_all(e)
        gms_consent_db.metadata.create_all(e)

if __name__ == "__main__":
    fire.Fire(ConsInsp)

