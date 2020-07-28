"""
project to coordinate inspection of the GMS consent forms
"""

import subprocess
import logging
import fire
from modules import log, attachment, jira, tickets
import local_config
from models import getEngine, makeSession, tk_db, gr_db

LOGGER = logging.getLogger(__name__)


def auto_model_gen(db_conn_str, schema, outfile):
    """
    Automatically generate sqlalchemy model from existing db
    :param db_conn_str: psycopg2-type connection string for db
    :param schema: schema to query
    :param outfile: the path to the file where model will be exported
    """

    LOGGER.info("Running auto_model_gen with arguments: %s > %s > %s"
                % (db_conn_str, schema, outfile))

    subprocess.call(["sqlacodegen", db_conn_str,
                     "--schema", schema,
                     "--outfile", outfile])


def list_to_table(l):
    """
    convert list of lists to jira markupstyle table (as list of lists),
    first element is the column names
    :param l: list of lists containing data to be transformed
    :returns: list of rows of table in jira markupstyle
    """

    # create list to return
    out = []

    for i in range(len(l)):

        if i == 0:
            out.append('||' + '||'.join(l[i]) + '||')
        else:
            out.append('|' + '|'.join(l[i]) + '|')

    return '\n'.join(out)


# Fire class of commandline arguments
class ConsInsp(object):

    def generate_gr_model(self, fn='models/gr_db.py'):
        """
        generate the gr_db SQLAlchemy model for the GR instance
        specified in the local_config file
        """

        LOGGER.info("Running generate_gr_model")

        auto_model_gen(local_config.gr_db_connection_string,
                       'public',
                       fn)


    def find_new_error_tickets(self):
        """
        find new error tickets generate during consent form checking and
        add them to the tracker database
        """

        s = makeSession()

        # get all the tickets we're interested in and those currently in db
        all_tickets = tickets.list_jira_issues(
            local_config.consent_form_check_errors_jql)
        db_tickets = s.query(tk_db.Ticket.ticket_key).all()
        db_tickets = [x[0] for x in db_tickets]

        # iterate through the new tickets
        for t in set(all_tickets) - set(db_tickets):

            # add the new ticket to the db
            n = tickets.NewTicket(t)
            n.update_db(s, 'inspection_fault')

        s.commit()


    def update_tickets(self):
        """
        Fetch all the tickets we know about and update details in db
        """

        s = makeSession()

        # get all the tickets from db
        existing_tickets = s.query(tk_db.Ticket)

        # update each ticket
        for t in existing_tickets:

            e = tickets.ExistingTicket(t)
            e.update_db()

        s.commit()


    def process_new_consent_forms(self):
        """
        Identify new consent forms and extract relevant parts into single
        inspection ticket
        """

        s = makeSession()

        # get the attachments that have already been processed
        db_attachments = s.query(tk_db.Attachment.uid).all()
        db_attachments = [x[0] for x in db_attachments]

        # query GR database to get all the consent forms that should be inspected
        # i.e. relevant title and not in db_attachments
        new_gr_attachments = s.query(gr_db.Attachment).\
            filter(gr_db.Attachment.attachment_title ==
                   'record-of-discussion-form.pdf').\
            filter(gr_db.Attachment.uid.notin_(db_attachments))

        # create objects that will be added to during processing
        attachment_objects = []
        jira_table = [['id', 'name', 'dob', 'image', 'fault link']]
        image_crops = []

        # iterate over each of the attachments in the query
        #TODO: remove limit here when we are over testing
        for i in new_gr_attachments[0:10]:

            # create instance of attachment class, doing so will do some
            # initial processing of the document
            c = attachment.Attachment(i, s)

            # extract participant info from GR db for the matching participant
            c.get_patient_info(s)

            if not c.errored:

                # if no errors have been raised then we can go ahead and add
                # it to what will go into the inspection ticket
                jira_table.append([str(c.attachment_id), c.person_name, c.dob,
                                   '!%s.png!' % c.attachment_id,
                                   '[Fault|%s]' % c.create_fault_ticket_url()])
                image_crops.append(('%s.png' % c.attachment_id,
                                    c.crop_page(1, 0.5, 0.5, 0.25, 0.25, 150)))
                attachment_objects.append(c)

            else:

                # if there are errors then we create an error ticket
                e = jira.ErrorTicket(s, c)
                e.create_ticket()

            # add details of the attachment to the database
            c.add_pages_to_db()

        if len(attachment_objects):

            # if we actually have any documents to inspect then we go ahead
            # and create an inspection ticket and add the attachments
            t = jira.InspectionTicket(s, jira_table, attachment_objects)
            t.tracking_db_ticket.attachments = [
                x.index_attachment for x in attachment_objects]
            t.ticket_image_attachments = image_crops
            t.create_ticket()

        s.commit()


    def create_tracker_db(self):
        """
        create the tracker db schema
        """

        LOGGER.info('Running recreateTrackerDB')

        e = getEngine(local_config.tk_db_connection_string)
        tk_db.metadata.drop_all(e)
        tk_db.metadata.create_all(e)


if __name__ == "__main__":
    fire.Fire(ConsInsp)
