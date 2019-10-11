# GMS Consent Inspections

These scripts generate the consent inspection tickets for any relevant attachments submitted during the early phases of GMS, and tracks any errors relating to the consent documents (corrupted pdfs etc.) and faults found in the consent documents during inspection.
The process is as follows:

1. source relevant attachment details from the Genomic Record database;
1. download the file from the S3 Bucket;
1. convert the pdf pages to image files and export to a filesystem;
1. link the attachment to patient and referral;
1. source relevant participant details from Genomic Record db;
1. crop out relevant portion of the form for inspection;
1. add to table in JIRA ticket with other new documents;
1. generate error tickets for any attachments that accumalate errors;
1. update the tracker database with fault tickets resulting from manual checking of the inspection tickets;
1. update details of each ticket in the tracker database by reading ticket data from JIRA.

The tracker database stores details of each attachment ingested, errors resulting from document inspection and processing, and the matching JIRA tickets.
