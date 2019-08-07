# GMS Consent Inspections

These scripts generate the consent inspection tickets for any relevant attachments submitted during the early phases of GMS.
The process is as follows:

1. source relevant attachment details from the Genomic Record database;
1. download the file from the S3 Bucket;
1. convert the pdf pages to image files and export to a filesystem;
1. link the attachment to patient and referral;
1. source relevant participant details from Genomic Record db;
1. crop out relevant portion of the form for inspection;
1. add to table in JIRA ticket with other new documents.

Any documents where any of the steps fail are the subject of a separate ticket.

A record of documents processed is stored on CDT's Index database.