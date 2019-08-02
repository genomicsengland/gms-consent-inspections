# db to store info on S3 buckets and process
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import datetime

Base = declarative_base()
metadata = Base.metadata

class attachment(Base):
    __tablename__ = 'attachment'
    __table_args__ = {'schema': 'dbs_consent_inspection'}

    file_id = Column(Integer, primary_key = True)
    attachment_uid = Column(UUID(as_uuid = True))
    attachment_title = Column(String)
    host_jira_ticket_id = Column(String)
    de_datetime = Column(DateTime, nullable = False, default = datetime.datetime.now())

    # one-to-one relationship with object on s3, one-to-many relationship with errors
    s3_object = relationship('s3Object', uselist = False, backref = 'attachment_object')
    errors = relationship('error', backref = 'attachment_error')

class s3Object(Base):
    __tablename__ = 's3_object'
    __table_args__ = {'schema': 'dbs_consent_inspection'}

    s3_object_id = Column(Integer, primary_key = True)
    file_id = Column(ForeignKey('dbs_consent_inspection.attachment.file_id'), nullable = False)
    s3_bucket = Column(String)
    s3_key = Column(String)
    last_modified = Column(DateTime)
    first_uid = Column(UUID(as_uuid = True))
    second_uid = Column(UUID(as_uuid = True))
    de_datetime = Column(DateTime, nullable = False, default = datetime.datetime.now())

    # one-to-one relationship with attachment, one-to-many relationship with fileImage
    images = relationship('fileImage', backref = 's3_object')

class fileImage(Base):
    __tablename__ = 'file_image'
    __table_args__ = {'schema': 'dbs_consent_inspection'}

    file_image_id = Column(Integer, primary_key = True)
    s3_object_id = Column(ForeignKey('dbs_consent_inspection.s3_object.s3_object_id'), nullable = False)
    path = Column(String)
    page_number = Column(Integer)
    page_empty = Column(Boolean)
    de_datetime = Column(DateTime, nullable = False, default = datetime.datetime.now())

class error(Base):
    __tablename__ = 'error'
    __table_args__ = {'schema': 'dbs_consent_inspection'}

    error_id = Column(Integer, primary_key = True)
    file_id = Column(ForeignKey('dbs_consent_inspection.attachment.file_id'), nullable = False)
    error_type = Column(String)
    error_status = Column(String)
    de_datetime = Column(DateTime, nullable = False, default = datetime.datetime.now())

