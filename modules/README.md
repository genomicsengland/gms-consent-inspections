# Modules

## attachment

The `attachment` module provides the `Attachment` class that is initiated with a `gr_db.Attachment` object and a SQLAlchemy session.
During initiation the attachment file is downloaded from the S3 Bucket (the path is provided by `gr_db.Attachment.attachment_url`), converted to a list of numpy arrays equivalent to grayscale images of each page (which are exported to PNG images), and a new instance of `gms_consent_db.Attachment` is added to the session.

The class provides methods to update the tracker database with details of the images generated, provide crops of particular portions of a page, and generate a direct HTML link for generating a JIRA Fault task.   

## jira

The `jira` module provides an `InspectionTicket` and `ErrorTicket` class, both of which inherit from the `Ticket` class.   
These classes hold information and attachments which will then be sent to JIRA to create a new ticket, and hold instances of `gms_consent_db.Ticket` that will be added to the tracker database.

## s3

The `s3` module holds various functions to work with files within the S3 Buckets.

## tickets

The `tickets` module holds two classes:

* `ExistingTicket` - a ticket that was created previously and exists within the tracker database, on initiation the class fetches updated data from JIRA which can be added to the database via the `updateDB` method;
* `NewTicket` - a ticket that exists on JIRA but is not recorded in the tracker database (i.e. a Fault ticket generated during consent form inspection), on initiation the class fetches data from JIRA and initiates a new instance of `gms_consent_db.Ticket` which is propagated to the tracker db (making a new instance of `gms_consent_db.Error` in the process) via the `updateDB` method.

