#!/usr/bin/env python3
#Scripts to help do the manual inspection of GMS consent forms
import fire
import logging
from modules import log
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
    """convert list of lists to jira markupstyle table, first element is the column names"""
    out = []
    for i in range(len(l)):
        if i == 0:
            out.append('||' + '||'.join(l[i]) + '||')
        else:
            out.append('|' + '|'.join(l[i]) + '|')
    return '\n'.join(out)

# create class that will become command argument with Fire
class ConsInsp(object):

    def generateGRModel(self, fn = 'models/gr_db.py'):
        """generate the gr_db SQLAlchemy model from the existing database"""
        logger.info("Running GenerateGRModel")
        autoModelGen(local_config.gr_db_connection_string,
                     'public',
                     fn)

    def FindNewTickets(self):
        """Find new error tickets and add them to db"""
        s = makeSession()
        # get all the tickets we're interested in and those currently in db
        all_tickets = tickets.listJiraIssues('project%20%3D%20"Clinical%20Data%20Wranglers%20%26%20Modellers"%20and%20summary%20~%20%27Consent%20Form%20Fault%27')
        existing_tickets = s.query(tk_db.Ticket.ticket_key).all()
        existing_tickets = [x[0] for x in existing_tickets]
        # iterate through all the tickets
        for t in all_tickets:
            if t not in existing_tickets:
                # else add the new ticket to the db
                n = tickets.NewTicket(t)
                n.updateDB(s, 'inspection_fault')
        s.commit()

    def UpdateTickets(self):
        """Fetch all the tickets we know about and update details"""
        s = makeSession()
        # get all the tickets we're interested in and those currently in db
        existing_tickets = s.query(tk_db.Ticket)
        # iterate through all the tickets
        for t in existing_tickets:
            # if already in the db, get it, then update the details
            e = tickets.ExistingTicket(t)
            e.updateDB()
        s.commit()

    def ProcessNewConsentForms(self):
        """Identify new consent forms and extract relevant parts into single ticket and write record to db"""
        s = makeSession()
        # get details on all the record of discussion forms in GR and TK db
        all_gr_attachments = s.query(gr_db.Attachment).\
            filter(gr_db.Attachment.attachment_title == 'record-of-discussion-form.pdf')
        known_attachments = s.query(tk_db.Attachment.gr_attachment_uid).all()
        known_attachments = [x[0] for x in known_attachments]
        # isolate the new attachments
        new_gr_attachments = [a for a in all_gr_attachments if a.uid not in known_attachments]
        # create objects that will be added to during processing
        attachment_objects = []
        jira_table = [['id', 'name', 'dob', 'image', 'fault link']]
        image_crops = []
        # iterate over each of the attachments in the query
        for i in new_gr_attachments[0:10]:
            # create instance of attachment class, doing so will do some initial processing of the document
            c = attachment.Attachment(i, s)
            # extract participant info from GR db for the matching participant
            c.extractParticipantInfo(s)
            if not c.errored:
                # if no errors have been raised then we can go ahead and add it to what will go into the inspection ticket
                jira_table.append([str(c.attachment_id), c.person_name, c.dob, '!%s.png!' % c.attachment_id, '[Fault|%s]' % c.createFaultTicketURL()])
                image_crops.append(('%s.png' % c.attachment_id, c.cropImageArea(1, 0.5, 0.5, 0.25, 0.25, 150))) 
                attachment_objects.append(c)
            else:
                # if there are errors then we crate an error ticket
                e = jira.ErrorTicket(s, c)
                e.createTicket()
            # add details of the attachment to the database
            c.updateDB()
        if len(attachment_objects):
            # if we actually have any documents to inspect then we go ahead and create an inspection ticket
            t = jira.InspectionTicket(s, jira_table, attachment_objects)
            t.tracking_db_ticket.attachments = [x.index_attachment for x in attachment_objects]
            t.ticket_image_attachments = image_crops
            t.createTicket()
        s.commit()

    def recreateTrackerDB(self):
        logger.info('Running recreateTrackerDB')
        e = getEngine(local_config.tk_db_connection_string)
        tk_db.metadata.drop_all(e)
        tk_db.metadata.create_all(e)

if __name__ == "__main__":
    fire.Fire(ConsInsp)

