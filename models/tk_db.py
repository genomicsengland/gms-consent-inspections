# db to store info on S3 buckets and process
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import datetime

Base = declarative_base()
metadata = Base.metadata

class Attachment(Base):
    __tablename__ = 'attachment'
    __table_args__ = {'schema': 'dbs_consent_inspection'}

    attachment_id = Column(Integer, primary_key = True)
    gr_attachment_uid = Column(UUID(as_uuid = True))
    s3_bucket = Column(String)
    s3_key = Column(String)
    patient_uid = Column(UUID(as_uuid = True))
    referral_uid = Column(UUID(as_uuid = True))
    ticket_id = Column(ForeignKey('dbs_consent_inspection.ticket.ticket_id'))
    de_datetime = Column(DateTime, nullable = False, default = datetime.datetime.now())

    # one-to-many relationship with images and errors
    errors = relationship('Error', backref = 'attachment_error')
    images = relationship('Image', backref = 'attachment_image')


class Image(Base):
    __tablename__ = 'image'
    __table_args__ = {'schema': 'dbs_consent_inspection'}

    image_id = Column(Integer, primary_key = True)
    attachment_id = Column(ForeignKey('dbs_consent_inspection.attachment.attachment_id'), nullable = False)
    path = Column(String)
    page_number = Column(Integer)
    page_empty = Column(Boolean)
    de_datetime = Column(DateTime, nullable = False, default = datetime.datetime.now())

class Error(Base):
    __tablename__ = 'error'
    __table_args__ = {'schema': 'dbs_consent_inspection'}

    error_id = Column(Integer, primary_key = True)
    attachment_id = Column(ForeignKey('dbs_consent_inspection.attachment.attachment_id'), nullable = False)
    error_type = Column(String)
    error_status = Column(String)
    ticket_id = Column(ForeignKey('dbs_consent_inspection.ticket.ticket_id'))
    de_datetime = Column(DateTime, nullable = False, default = datetime.datetime.now())

class Ticket(Base):
    __tablename__ = 'ticket'
    __table_args__ = {'schema': 'dbs_consent_inspection'}

    ticket_id = Column(Integer, primary_key = True)
    ticket_key = Column(String, nullable = False)
    ticket_status = Column(String)
    ticket_assignee = Column(String)
    ticket_updated = Column(DateTime)
    de_datetime = Column(DateTime, nullable = False, default = datetime.datetime.now())

    #one-to-many relationship with attachments and errors
    attachments = relationship('Attachment', backref = 'ticket_attachment')
    errors = relationship('Error', backref = 'ticket_error')
