#!/usr/bin/env python3
#Scripts to help do the manual inspection of GMS consent forms
import fire
import logging
import log
import subprocess
import local_config
from sqlalchemy.orm import sessionmaker
from modules import s3, attachment, jira, tickets
from models import getEngine, makeSession, tk_db, gr_db

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

# create class that will become command argument with Fire
# e.g. python3 ngis_mq.py RunReferralTests
class ConsInsp(object):

    def generateGRModel(self, fn = 'models/gr_db.py'):
        """generate the gr_db model"""
        logger.info("Running GenerateGRModel")
        autoModelGen(local_config.gr_db_connection_string,
                     'public',
                     fn)

    def checkForFaultTickets(self):
        s = makeSession()
        all_tickets = tickets.listJiraIssues('summary%20~%20%27Consent%20Form%20Fault%27') 
        existing_tickets = s.query(tk_db.Ticket.ticket_key).all()
        existing_tickets = [x[0] for x in existing_tickets]
        new_tickets = [x for x in all_tickets if x not in existing_tickets]
        for i in new_tickets:
            n = tickets.NewTicket(i)
            n.updateDB(s, 'inspection_fault')
        s.commit()

    def inspectExistingTickets(self):
        # get new tickets we didn't know about
        s = makeSession()
        new_tickets = tickets.listJiraIssues('summary%20~%20%27Consent%20Form%20Fault%27') 
        for i in new_tickets:
            a = tk_db.Ticket(ticket_key = i)
            s.add(a)
        q = s.query(tk_db.Ticket)
        for t in q:
            logger.info('Checking %s' % t.ticket_key)
            e = tickets.ExistingTicket(t)
            e.updateDB()
        s.commit()


    def process(self):
        s = makeSession()
        test_uids = s.query(gr_db.Attachment).\
            filter(gr_db.Attachment.attachment_title == 'record-of-discussion-form.pdf')
        objects = []
        table = [['id', 'name', 'dob', 'image', 'fault link']]
        crops = []
        for i in test_uids[0:10]:
            c = attachment.Attachment(i, s)
            c.extractParticipantInfo(s)
            if not c.errored:
                table.append([str(c.attachment_id), c.person_name, c.dob, '!%s.png!' % c.attachment_id, '[Fault|%s]' % c.createFaultTicketURL()])
                crops.append(('%s.png' % c.attachment_id, c.cropImageArea(1, 0.5, 0.5, 0.25, 0.25, 150))) 
                objects.append(c)
            else:
                e = jira.ErrorTicket(s, c)
                e.createTicket()
            c.updateDB()
        if len(objects):
            t = jira.InspectionTicket(s, table, objects)
            t.tracking_db_ticket.attachments = [x.index_attachment for x in objects]
            t.ticket_image_attachments = crops
            t.createTicket()
        s.commit()

    def recreateConsentDB(self):
        logger.info('Running recreateConsentDB')
        e = getEngine(local_config.tk_db_connection_string)
        tk_db.metadata.drop_all(e)
        tk_db.metadata.create_all(e)

if __name__ == "__main__":
    fire.Fire(ConsInsp)

