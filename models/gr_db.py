# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKey, Integer, LargeBinary, Numeric, SmallInteger, String, Table, Text, Time, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Addres(Base):
    __tablename__ = 'address'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    address_line_1 = Column(Text)
    address_line_2 = Column(Text)
    address_line_3 = Column(Text)
    address_line_4 = Column(Text)
    address_line_5 = Column(Text)
    address_postcode = Column(Text, index=True)
    address_date_effective_from = Column(Date, nullable=False)
    address_date_effective_to = Column(Date)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)


class AddressVersion(Base):
    __tablename__ = 'address_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    address_line_1 = Column(Text)
    address_line_2 = Column(Text)
    address_line_3 = Column(Text)
    address_line_4 = Column(Text)
    address_line_5 = Column(Text)
    address_postcode = Column(Text, index=True)
    address_date_effective_from = Column(Date)
    address_date_effective_to = Column(Date)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    address_line_1_mod = Column(Boolean, nullable=False, server_default=text("false"))
    address_line_2_mod = Column(Boolean, nullable=False, server_default=text("false"))
    address_line_3_mod = Column(Boolean, nullable=False, server_default=text("false"))
    address_line_4_mod = Column(Boolean, nullable=False, server_default=text("false"))
    address_line_5_mod = Column(Boolean, nullable=False, server_default=text("false"))
    address_postcode_mod = Column(Boolean, nullable=False, server_default=text("false"))
    address_date_effective_from_mod = Column(Boolean, nullable=False, server_default=text("false"))
    address_date_effective_to_mod = Column(Boolean, nullable=False, server_default=text("false"))


class AttachmentVersion(Base):
    __tablename__ = 'attachment_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    attachment_content_type = Column(Text)
    attachment_data = Column(LargeBinary)
    attachment_url = Column(Text)
    attachment_size = Column(Integer)
    attachment_hash = Column(LargeBinary)
    attachment_title = Column(Text)
    attachment_created = Column(DateTime)
    attachment_type_cid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    attachment_content_type_mod = Column(Boolean, nullable=False, server_default=text("false"))
    attachment_data_mod = Column(Boolean, nullable=False, server_default=text("false"))
    attachment_url_mod = Column(Boolean, nullable=False, server_default=text("false"))
    attachment_size_mod = Column(Boolean, nullable=False, server_default=text("false"))
    attachment_hash_mod = Column(Boolean, nullable=False, server_default=text("false"))
    attachment_title_mod = Column(Boolean, nullable=False, server_default=text("false"))
    attachment_created_mod = Column(Boolean, nullable=False, server_default=text("false"))
    attachment_type_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class AwsdmsDdlAudit(Base):
    __tablename__ = 'awsdms_ddl_audit'
    __table_args__ = {'schema': 'public'}

    c_key = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".awsdms_ddl_audit_c_key_seq'::regclass)"))
    c_time = Column(DateTime)
    c_user = Column(String(64))
    c_txn = Column(String(16))
    c_tag = Column(String(24))
    c_oid = Column(Integer)
    c_name = Column(String(64))
    c_schema = Column(String(64))
    c_ddlqry = Column(Text)


class CdrAuthorVersion(Base):
    __tablename__ = 'cdr_author_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    consent_document_reference_uid = Column(UUID)
    identifier_uid = Column(UUID)
    cdr_author_type_cid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_document_reference_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    identifier_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cdr_author_type_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class CdrContentVersion(Base):
    __tablename__ = 'cdr_content_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    consent_document_reference_uid = Column(UUID)
    attachment_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_document_reference_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    attachment_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class CdrRelatesToVersion(Base):
    __tablename__ = 'cdr_relates_to_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    code_cid = Column(UUID)
    consent_document_reference_uid = Column(UUID)
    identifier_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    code_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_document_reference_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    identifier_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ClinicalEthnicityVersion(Base):
    __tablename__ = 'clinical_ethnicity_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    patient_uid = Column(UUID)
    clinical_ethnicity_cid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    clinical_ethnicity_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class Clinician(Base):
    __tablename__ = 'clinician'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    clinician_forename = Column(Text)
    clinician_surname = Column(Text, nullable=False)
    clinician_departmental_address = Column(Text)
    clinician_profession_registration_number = Column(Text)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    clinician_email_address = Column(String(255))
    clinician_phone_number = Column(Text)
    last_updated = Column(DateTime, index=True)
    organisation_uid = Column(UUID)


class ClinicianVersion(Base):
    __tablename__ = 'clinician_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    clinician_forename = Column(Text)
    clinician_surname = Column(Text)
    clinician_email_address = Column(String(255))
    clinician_phone_number = Column(Text)
    clinician_departmental_address = Column(Text)
    clinician_profession_registration_number = Column(Text)
    organisation_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    clinician_forename_mod = Column(Boolean, nullable=False, server_default=text("false"))
    clinician_surname_mod = Column(Boolean, nullable=False, server_default=text("false"))
    clinician_email_address_mod = Column(Boolean, nullable=False, server_default=text("false"))
    clinician_phone_number_mod = Column(Boolean, nullable=False, server_default=text("false"))
    clinician_departmental_address_mod = Column(Boolean, nullable=False, server_default=text("false"))
    clinician_profession_registration_number_mod = Column(Boolean, nullable=False, server_default=text("false"))
    organisation_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class Codesystem(Base):
    __tablename__ = 'codesystem'
    __table_args__ = {'schema': 'public'}

    codesystem_uri = Column(String(255), primary_key=True)
    codesystem_version = Column(Text)
    codesystem_name = Column(Text)


class ConditionVersion(Base):
    __tablename__ = 'condition_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    condition_clinical_status_cid = Column(UUID)
    condition_verification_status_cid = Column(UUID)
    condition_category_code_cid = Column(UUID)
    condition_certainty_cid = Column(UUID)
    condition_code_cid = Column(UUID)
    condition_body_site_code_cid = Column(UUID)
    patient_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    condition_clinical_status_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    condition_verification_status_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    condition_category_code_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    condition_certainty_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    condition_code_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    condition_body_site_code_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ConsentDocumentReferenceVersion(Base):
    __tablename__ = 'consent_document_reference_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(UUID)
    identifier_uid = Column(UUID)
    status_cid = Column(UUID)
    indexed = Column(DateTime)
    description = Column(Text)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    identifier_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    status_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    indexed_mod = Column(Boolean, nullable=False, server_default=text("false"))
    description_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ConsentNoteVersion(Base):
    __tablename__ = 'consent_note_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(UUID)
    consent_note_text = Column(Text)
    consent_note_time = Column(DateTime)
    identifier_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_note_text_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_note_time_mod = Column(Boolean, nullable=False, server_default=text("false"))
    identifier_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ConsentOrganisationVersion(Base):
    __tablename__ = 'consent_organisation_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(UUID)
    identifier_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    identifier_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ConsentQuestionnaireResponseVersion(Base):
    __tablename__ = 'consent_questionnaire_response_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(UUID)
    identifier_uid = Column(UUID)
    consent_questionnaire_uid = Column(UUID)
    status_cid = Column(UUID)
    consent_questionnaire_response_authored = Column(DateTime)
    source_identifier_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    identifier_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_questionnaire_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    status_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_questionnaire_response_authored_mod = Column(Boolean, nullable=False, server_default=text("false"))
    source_identifier_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ConsentQuestionnaireVersion(Base):
    __tablename__ = 'consent_questionnaire_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    identifier_uid = Column(UUID)
    version = Column(Text)
    name = Column(Text)
    title = Column(Text)
    status_cid = Column(UUID)
    changed = Column(DateTime)
    description = Column(Text)
    purpose = Column(Text)
    approval_date = Column(DateTime)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    identifier_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    version_mod = Column(Boolean, nullable=False, server_default=text("false"))
    name_mod = Column(Boolean, nullable=False, server_default=text("false"))
    title_mod = Column(Boolean, nullable=False, server_default=text("false"))
    status_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    changed_mod = Column(Boolean, nullable=False, server_default=text("false"))
    description_mod = Column(Boolean, nullable=False, server_default=text("false"))
    purpose_mod = Column(Boolean, nullable=False, server_default=text("false"))
    approval_date_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ConsentVersion(Base):
    __tablename__ = 'consent_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    patient_uid = Column(UUID)
    identifier_uid = Column(UUID)
    status_cid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    identifier_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    status_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ConsentWitnessVersion(Base):
    __tablename__ = 'consent_witness_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(UUID)
    consent_witness_url = Column(Text)
    identifier_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_witness_url_mod = Column(Boolean, nullable=False, server_default=text("false"))
    identifier_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ConsentingPartyVersion(Base):
    __tablename__ = 'consenting_party_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(UUID)
    identifier_uid = Column(UUID)
    relationship_cid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    identifier_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    relationship_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ContactVersion(Base):
    __tablename__ = 'contact_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    patient_uid = Column(UUID)
    contact_person_uid = Column(UUID)
    relationship_type_cid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    contact_person_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    relationship_type_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class CqItemEnableWhenVersion(Base):
    __tablename__ = 'cq_item_enable_when_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    cq_item_uid = Column(UUID)
    cq_item_enable_when_question = Column(Text)
    cq_item_enable_when_has_answer = Column(Boolean)
    cq_item_enable_when_answer_bool = Column(Boolean)
    cq_item_enable_when_answer_integer = Column(Integer)
    cq_item_enable_when_answer_decimal = Column(Numeric)
    cq_item_enable_when_answer_string = Column(Text)
    cq_item_enable_when_answer_date = Column(Date)
    cq_item_enable_when_answer_datetime = Column(DateTime)
    cq_item_enable_when_answer_time = Column(Time)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_enable_when_question_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_enable_when_has_answer_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_enable_when_answer_bool_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_enable_when_answer_integer_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_enable_when_answer_decimal_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_enable_when_answer_string_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_enable_when_answer_date_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_enable_when_answer_datetime_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_enable_when_answer_time_mod = Column(Boolean, nullable=False, server_default=text("false"))


class CqItemOptionVersion(Base):
    __tablename__ = 'cq_item_option_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    cq_item_uid = Column(UUID)
    cq_item_option_value_integer = Column(Integer)
    cq_item_option_value_string = Column(Text)
    cq_item_option_value_date = Column(Date)
    cq_item_option_value_time = Column(Time)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_option_value_integer_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_option_value_string_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_option_value_date_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_option_value_time_mod = Column(Boolean, nullable=False, server_default=text("false"))


class CqItemVersion(Base):
    __tablename__ = 'cq_item_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    consent_questionnaire_uid = Column(UUID)
    cq_item_link_id = Column(Text)
    cq_item_prefix = Column(Text)
    cq_item_text = Column(Text)
    cq_item_type_cid = Column(UUID)
    cq_item_required = Column(Boolean)
    cq_item_read_only = Column(Boolean)
    cq_item_max_length = Column(Integer)
    cq_parent_item_uid = Column(UUID)
    cq_item_initial_bool = Column(Boolean)
    cq_item_initial_integer = Column(Integer)
    cq_item_initial_string = Column(Text)
    cq_item_initial_decimal = Column(Numeric)
    cq_item_initial_date = Column(Date)
    cq_item_initial_datetime = Column(DateTime)
    cq_item_initial_time = Column(Time)
    initial_attachment_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_questionnaire_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_link_id_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_prefix_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_text_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_type_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_required_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_read_only_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_max_length_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_parent_item_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_initial_bool_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_initial_integer_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_initial_string_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_initial_decimal_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_initial_date_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_initial_datetime_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cq_item_initial_time_mod = Column(Boolean, nullable=False, server_default=text("false"))
    initial_attachment_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class CqrAnswerVersion(Base):
    __tablename__ = 'cqr_answer_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    cqr_item_uid = Column(UUID, index=True)
    value_bool = Column(Boolean)
    value_decimal = Column(Numeric)
    value_integer = Column(Integer)
    value_date = Column(Date)
    value_datetime = Column(DateTime)
    value_time = Column(Time)
    value_string = Column(Text)
    value_attachment_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cqr_item_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    value_bool_mod = Column(Boolean, nullable=False, server_default=text("false"))
    value_decimal_mod = Column(Boolean, nullable=False, server_default=text("false"))
    value_integer_mod = Column(Boolean, nullable=False, server_default=text("false"))
    value_date_mod = Column(Boolean, nullable=False, server_default=text("false"))
    value_datetime_mod = Column(Boolean, nullable=False, server_default=text("false"))
    value_time_mod = Column(Boolean, nullable=False, server_default=text("false"))
    value_string_mod = Column(Boolean, nullable=False, server_default=text("false"))
    value_attachment_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class CqrAuthorVersion(Base):
    __tablename__ = 'cqr_author_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    consent_questionnaire_response_uid = Column(UUID)
    identifier_uid = Column(UUID)
    author_type_cid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_questionnaire_response_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    identifier_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    author_type_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class CqrBasedOnVersion(Base):
    __tablename__ = 'cqr_based_on_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    consent_questionnaire_response_uid = Column(UUID)
    identifier_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_questionnaire_response_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    identifier_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class CqrItemVersion(Base):
    __tablename__ = 'cqr_item_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    cqr_parent_item_uid = Column(UUID, index=True)
    consent_questionnaire_response_uid = Column(UUID)
    cqr_item_link_id = Column(Text)
    cqr_item_text = Column(Text)
    subject_identifier_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cqr_parent_item_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_questionnaire_response_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cqr_item_link_id_mod = Column(Boolean, nullable=False, server_default=text("false"))
    cqr_item_text_mod = Column(Boolean, nullable=False, server_default=text("false"))
    subject_identifier_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


t_db_version = Table(
    'db_version', metadata,
    Column('version', Text),
    schema='public'
)


class IdentifierVersion(Base):
    __tablename__ = 'identifier_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    polymorphic_type = Column(Text)
    value = Column(Text)
    organisation_uid = Column(UUID)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    condition_uid = Column(UUID)
    observation_uid = Column(UUID)
    patient_uid = Column(UUID)
    referral_uid = Column(UUID)
    sample_uid = Column(UUID)
    tumour_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    polymorphic_type_mod = Column(Boolean, nullable=False, server_default=text("false"))
    value_mod = Column(Boolean, nullable=False, server_default=text("false"))
    organisation_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    period_start_mod = Column(Boolean, nullable=False, server_default=text("false"))
    period_end_mod = Column(Boolean, nullable=False, server_default=text("false"))
    condition_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    observation_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    sample_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    tumour_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    type_cid = Column(UUID)
    type_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))


t_mi_referral = Table(
    'mi_referral', metadata,
    Column('uid', UUID),
    Column('date_request_submitted', Date),
    Column('ordering_entity', UUID),
    Column('referral_id', String),
    Column('priority_flag', Text),
    Column('clinical_indication_uid', UUID),
    Column('referral_created_at', Date),
    Column('date_last_submitted', Date),
    Column('status', Text),
    Column('ci_test_type_uid', UUID),
    Column('sample_processing_lab_uid', UUID),
    schema='public'
)


t_mi_sample = Table(
    'mi_sample', metadata,
    Column('patient_uid', UUID),
    Column('tumour_uid', UUID),
    Column('ngis_sample_id', UUID),
    Column('sample_type', Text),
    Column('sample_state', Text),
    Column('sample_collection_date', DateTime),
    Column('value', Text),
    Column('order_id', Integer),
    Column('local_lab_germline_sample_id', Text),
    schema='public'
)


class ObservationComponentVersion(Base):
    __tablename__ = 'observation_component_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    observation_uid = Column(UUID)
    observation_component_code_cid = Column(UUID)
    observation_component_value_string = Column(Text)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    observation_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    observation_component_code_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    observation_component_value_string_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ObservationVersion(Base):
    __tablename__ = 'observation_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    patient_uid = Column(UUID)
    observation_effective_from = Column(Date)
    observation_effective_to = Column(Date)
    observation_code_cid = Column(UUID)
    observation_value_code_cid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    observation_effective_from_mod = Column(Boolean, nullable=False, server_default=text("false"))
    observation_effective_to_mod = Column(Boolean, nullable=False, server_default=text("false"))
    observation_code_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    observation_value_code_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class OrganisationConsentVersion(Base):
    __tablename__ = 'organisation_consent_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    organisation_uid = Column(UUID)
    consent_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    organisation_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consent_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class PatientVersion(Base):
    __tablename__ = 'patient_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    patient_created_at = Column(Date)
    patient_human_readable_stored_id = Column(String, server_default=text("patient_human_readable_id('patient_human_readable_id_sequence'::regclass)"))
    patient_date_of_birth = Column(Date)
    patient_date_of_death = Column(Date)
    patient_is_foetal_patient = Column(Boolean)
    patient_fetus_current_gestation = Column(Integer)
    patient_fetus_current_gestation_unit = Column(Text)
    patient_fetus_estimated_due_date = Column(Date)
    patient_last_menstrual_period = Column(Date)
    additional_data = Column(JSONB(astext_type=Text()))
    person_uid = Column(UUID)
    administrative_gender_cid = Column(UUID)
    ethnicity_cid = Column(UUID)
    phenotypic_sex_cid = Column(UUID)
    karyotypic_sex_cid = Column(UUID)
    address_uid = Column(UUID)
    life_status_cid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_created_at_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_human_readable_stored_id_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_date_of_birth_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_date_of_death_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_is_foetal_patient_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_fetus_current_gestation_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_fetus_current_gestation_unit_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_fetus_estimated_due_date_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_last_menstrual_period_mod = Column(Boolean, nullable=False, server_default=text("false"))
    additional_data_mod = Column(Boolean, nullable=False, server_default=text("false"))
    person_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    administrative_gender_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    ethnicity_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    phenotypic_sex_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    karyotypic_sex_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    address_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    life_status_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class PersonVersion(Base):
    __tablename__ = 'person_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    address_uid = Column(UUID)
    person_name_prefix = Column(Text)
    person_first_name = Column(Text)
    person_middle_name = Column(Text)
    person_family_name = Column(Text)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    address_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    person_name_prefix_mod = Column(Boolean, nullable=False, server_default=text("false"))
    person_first_name_mod = Column(Boolean, nullable=False, server_default=text("false"))
    person_middle_name_mod = Column(Boolean, nullable=False, server_default=text("false"))
    person_family_name_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ProcedureRequestVersion(Base):
    __tablename__ = 'procedure_request_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    referral_participant_uid = Column(UUID)
    referral_test_uid = Column(UUID)
    additional_data = Column(JSONB(astext_type=Text()))
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_participant_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_test_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    additional_data_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ReferralAdditionalClinicianVersion(Base):
    __tablename__ = 'referral_additional_clinician_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    referral_uid = Column(UUID)
    clinician_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    clinician_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ReferralAttachmentVersion(Base):
    __tablename__ = 'referral_attachment_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    referral_uid = Column(UUID)
    attachment_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    attachment_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ReferralPanelVersion(Base):
    __tablename__ = 'referral_panel_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    referral_test_uid = Column(UUID)
    referral_panel_id = Column(Text)
    referral_panel_display = Column(Text)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_test_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_panel_id_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_panel_display_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ReferralParticipantAttachmentVersion(Base):
    __tablename__ = 'referral_participant_attachment_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    referral_participant_uid = Column(UUID)
    attachment_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_participant_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    attachment_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ReferralParticipantVersion(Base):
    __tablename__ = 'referral_participant_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    referral_uid = Column(UUID)
    patient_uid = Column(UUID)
    referral_participant_is_proband = Column(Boolean)
    additional_data = Column(JSONB(astext_type=Text()))
    relationship_to_proband_cid = Column(UUID)
    referral_participant_other_relationship_details = Column(Text)
    disease_status_cid = Column(UUID)
    referral_participant_age_at_onset = Column(Integer)
    consanguinity_cid = Column(UUID)
    mother_affected_cid = Column(UUID)
    father_affected_cid = Column(UUID)
    referral_participant_full_brother_count = Column(Integer)
    referral_participant_full_brothers_affected = Column(Integer)
    referral_participant_full_sister_count = Column(Integer)
    referral_participant_full_sisters_affected = Column(Integer)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_participant_is_proband_mod = Column(Boolean, nullable=False, server_default=text("false"))
    additional_data_mod = Column(Boolean, nullable=False, server_default=text("false"))
    relationship_to_proband_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_participant_other_relationship_details_mod = Column(Boolean, nullable=False, server_default=text("false"))
    disease_status_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_participant_age_at_onset_mod = Column(Boolean, nullable=False, server_default=text("false"))
    consanguinity_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    mother_affected_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    father_affected_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_participant_full_brother_count_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_participant_full_brothers_affected_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_participant_full_sister_count_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_participant_full_sisters_affected_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ReferralSampleVersion(Base):
    __tablename__ = 'referral_sample_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    sample_uid = Column(UUID)
    referral_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    sample_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ReferralTestTargetRegionVersion(Base):
    __tablename__ = 'referral_test_target_region_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    referral_test_uid = Column(UUID)
    referral_test_target_region = Column(Text)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_test_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_test_target_region_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ReferralTestTargetVariantVersion(Base):
    __tablename__ = 'referral_test_target_variant_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    referral_test_uid = Column(UUID)
    referral_test_target_variant = Column(Text)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_test_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_test_target_variant_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ReferralTestVersion(Base):
    __tablename__ = 'referral_test_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    referral_test_expected_number_of_patients = Column(Integer)
    ci_test_type_uid = Column(UUID)
    referral_uid = Column(UUID)
    penetrance_cid = Column(UUID)
    status_cid = Column(UUID)
    referral_test_medical_review_qc_state_cid = Column(UUID)
    additional_data = Column(JSONB(astext_type=Text()))
    interpretation_lab_uid = Column(UUID)
    sample_processing_lab_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_test_expected_number_of_patients_mod = Column(Boolean, nullable=False, server_default=text("false"))
    ci_test_type_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    penetrance_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    status_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_test_medical_review_qc_state_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    additional_data_mod = Column(Boolean, nullable=False, server_default=text("false"))
    interpretation_lab_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    sample_processing_lab_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class ReferralVersion(Base):
    __tablename__ = 'referral_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    parent_referral_uid = Column(UUID)
    referral_created_at = Column(Date)
    referral_human_readable_stored_id = Column(String, server_default=text("referral_human_readable_id('referral_human_readable_id_sequence'::regclass)"))
    status_cid = Column(UUID)
    intent_cid = Column(UUID)
    priority_cid = Column(UUID)
    clinical_indication_uid = Column(UUID)
    responsible_clinician_uid = Column(UUID)
    tumour_uid = Column(UUID)
    ordering_entity_uid = Column(UUID)
    reason_declined_cid = Column(UUID)
    referral_date_last_submitted = Column(Date)
    referral_date_submitted = Column(Date)
    referral_occurrence_start = Column(Date)
    referral_notes = Column(Text)
    referral_is_prenatal_test = Column(Boolean)
    referral_expected_number_of_samples = Column(Integer)
    additional_data = Column(JSONB(astext_type=Text()))
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    parent_referral_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_created_at_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_human_readable_stored_id_mod = Column(Boolean, nullable=False, server_default=text("false"))
    status_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    intent_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    priority_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    clinical_indication_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    responsible_clinician_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    tumour_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    ordering_entity_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    reason_declined_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_date_last_submitted_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_date_submitted_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_occurrence_start_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_notes_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_is_prenatal_test_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_expected_number_of_samples_mod = Column(Boolean, nullable=False, server_default=text("false"))
    additional_data_mod = Column(Boolean, nullable=False, server_default=text("false"))


class RelatedPersonVersion(Base):
    __tablename__ = 'related_person_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    source_patient_uid = Column(UUID)
    target_person_uid = Column(UUID)
    relationship_type_cid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    source_patient_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    target_person_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    relationship_type_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class SampleVersion(Base):
    __tablename__ = 'sample_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    patient_uid = Column(UUID)
    tumour_uid = Column(UUID)
    parent_uid = Column(UUID)
    percentage_of_malignant_cells = Column(Integer)
    sample_type_cid = Column(UUID)
    sample_topography_cid = Column(UUID)
    sample_morphology_cid = Column(UUID)
    sample_state_cid = Column(UUID)
    sample_number_of_slides = Column(Integer)
    sample_collection_date = Column(DateTime)
    sample_notes = Column(Text)
    sample_ready_for_dispatch = Column(Boolean)
    sample_shipping_status_cid = Column(UUID)
    sample_requested_for_other_test = Column(Boolean)
    other_referral_request_uid = Column(UUID)
    body_site_cid = Column(UUID)
    additional_data = Column(JSONB(astext_type=Text()))
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    tumour_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    parent_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    percentage_of_malignant_cells_mod = Column(Boolean, nullable=False, server_default=text("false"))
    sample_type_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    sample_topography_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    sample_morphology_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    sample_state_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    sample_number_of_slides_mod = Column(Boolean, nullable=False, server_default=text("false"))
    sample_collection_date_mod = Column(Boolean, nullable=False, server_default=text("false"))
    sample_notes_mod = Column(Boolean, nullable=False, server_default=text("false"))
    sample_ready_for_dispatch_mod = Column(Boolean, nullable=False, server_default=text("false"))
    sample_shipping_status_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    sample_requested_for_other_test_mod = Column(Boolean, nullable=False, server_default=text("false"))
    other_referral_request_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    body_site_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    additional_data_mod = Column(Boolean, nullable=False, server_default=text("false"))


class SequenceStatu(Base):
    __tablename__ = 'sequence_status'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    sequence_status_name = Column(String(255), nullable=False, unique=True)
    sequence_status_last_reset = Column(DateTime, nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)


class SequenceStatusVersion(Base):
    __tablename__ = 'sequence_status_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    sequence_status_name = Column(String(255))
    sequence_status_last_reset = Column(DateTime)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    sequence_status_name_mod = Column(Boolean, nullable=False, server_default=text("false"))
    sequence_status_last_reset_mod = Column(Boolean, nullable=False, server_default=text("false"))


class Technology(Base):
    __tablename__ = 'technology'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))


class TelecomVersion(Base):
    __tablename__ = 'telecom_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    person_uid = Column(UUID)
    system_cid = Column(UUID)
    telecom_value = Column(Text)
    use_cid = Column(UUID)
    telecom_rank = Column(Integer)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    person_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    system_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    telecom_value_mod = Column(Boolean, nullable=False, server_default=text("false"))
    use_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    telecom_rank_mod = Column(Boolean, nullable=False, server_default=text("false"))


class Transaction(Base):
    __tablename__ = 'transaction'
    __table_args__ = {'schema': 'public'}

    issued_at = Column(DateTime)
    id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"public\".transaction_id_seq'::regclass)"))
    remote_addr = Column(String(50))


class TransactionChange(Base):
    __tablename__ = 'transaction_changes'
    __table_args__ = {'schema': 'public'}

    transaction_id = Column(BigInteger, primary_key=True, nullable=False)
    entity_name = Column(String(255), primary_key=True, nullable=False)


class TumourDescriptionVersion(Base):
    __tablename__ = 'tumour_description_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    tumour_uid = Column(UUID)
    tumour_description = Column(Text)
    referral_uid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    tumour_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    tumour_description_mod = Column(Boolean, nullable=False, server_default=text("false"))
    referral_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class TumourLabResultVersion(Base):
    __tablename__ = 'tumour_lab_result_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    tumour_uid = Column(UUID)
    organisation_uid = Column(UUID)
    clinician_uid = Column(UUID)
    flow_cytometry_marker_name = Column(Text)
    flow_cytometry_result_cid = Column(UUID)
    immunohistochemistry_marker = Column(Text)
    immunohistochemistry_result_cid = Column(UUID)
    immunohistochemistry_results_percentage = Column(Integer)
    fish_target = Column(Text)
    fish_findings_cid = Column(UUID)
    fish_detected = Column(Boolean)
    number_cells_examined = Column(Integer)
    number_cells_detected_in = Column(Integer)
    number_copies_detected = Column(Integer)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    tumour_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    organisation_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    clinician_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    flow_cytometry_marker_name_mod = Column(Boolean, nullable=False, server_default=text("false"))
    flow_cytometry_result_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    immunohistochemistry_marker_mod = Column(Boolean, nullable=False, server_default=text("false"))
    immunohistochemistry_result_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    immunohistochemistry_results_percentage_mod = Column(Boolean, nullable=False, server_default=text("false"))
    fish_target_mod = Column(Boolean, nullable=False, server_default=text("false"))
    fish_findings_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    fish_detected_mod = Column(Boolean, nullable=False, server_default=text("false"))
    number_cells_examined_mod = Column(Boolean, nullable=False, server_default=text("false"))
    number_cells_detected_in_mod = Column(Boolean, nullable=False, server_default=text("false"))
    number_copies_detected_mod = Column(Boolean, nullable=False, server_default=text("false"))


class TumourMorphologyVersion(Base):
    __tablename__ = 'tumour_morphology_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    tumour_uid = Column(UUID)
    morphology_cid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    tumour_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    morphology_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class TumourTopographyVersion(Base):
    __tablename__ = 'tumour_topography_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    tumour_uid = Column(UUID)
    actual_body_site_cid = Column(UUID)
    primary_body_site_cid = Column(UUID)
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    tumour_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    actual_body_site_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    primary_body_site_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))


class TumourVersion(Base):
    __tablename__ = 'tumour_version'
    __table_args__ = {'schema': 'public'}

    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    patient_uid = Column(UUID)
    presentation_cid = Column(UUID)
    _type_cid = Column(UUID)
    tumour_diagnosis_year = Column(Text)
    tumour_diagnosis_month = Column(Text)
    tumour_diagnosis_day = Column(Text)
    diagnosis_age_in_years = Column(Integer)
    grade_cid = Column(UUID)
    stage_cid = Column(UUID)
    prognostic_score_cid = Column(UUID)
    parent_tumour_uid = Column(UUID)
    organisation_uid = Column(UUID)
    clinician_uid = Column(UUID)
    additional_data = Column(JSONB(astext_type=Text()))
    transaction_id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    end_transaction_id = Column(BigInteger, index=True)
    operation_type = Column(SmallInteger, nullable=False, index=True)
    last_updated_by_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_by_session_mod = Column(Boolean, nullable=False, server_default=text("false"))
    last_updated_mod = Column(Boolean, nullable=False, server_default=text("false"))
    patient_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    presentation_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    _type_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    tumour_diagnosis_year_mod = Column(Boolean, nullable=False, server_default=text("false"))
    tumour_diagnosis_month_mod = Column(Boolean, nullable=False, server_default=text("false"))
    tumour_diagnosis_day_mod = Column(Boolean, nullable=False, server_default=text("false"))
    diagnosis_age_in_years_mod = Column(Boolean, nullable=False, server_default=text("false"))
    grade_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    stage_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    prognostic_score_cid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    parent_tumour_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    organisation_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    clinician_uid_mod = Column(Boolean, nullable=False, server_default=text("false"))
    additional_data_mod = Column(Boolean, nullable=False, server_default=text("false"))


class Concept(Base):
    __tablename__ = 'concept'
    __table_args__ = (
        UniqueConstraint('concept_code', 'codesystem_uri'),
        {'schema': 'public'}
    )

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    concept_code = Column(Text, nullable=False)
    concept_display = Column(Text, nullable=False)
    codesystem_uri = Column(ForeignKey('public.codesystem.codesystem_uri'), nullable=False)
    concept_sort_order = Column(Integer, nullable=False, server_default=text("0"))

    codesystem = relationship('Codesystem')


class Person(Base):
    __tablename__ = 'person'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    address_uid = Column(ForeignKey('public.address.uid', ondelete='SET NULL'))
    person_family_name = Column(Text, nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    person_first_name = Column(Text)
    person_middle_name = Column(Text)
    person_name_prefix = Column(Text)

    addres = relationship('Addres')


class Attachment(Base):
    __tablename__ = 'attachment'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    attachment_content_type = Column(Text)
    attachment_data = Column(LargeBinary)
    attachment_url = Column(Text)
    attachment_size = Column(Integer)
    attachment_hash = Column(LargeBinary)
    attachment_title = Column(Text)
    attachment_created = Column(DateTime)
    attachment_type_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept')


class Patient(Base):
    __tablename__ = 'patient'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    person_uid = Column(ForeignKey('public.person.uid'), nullable=False)
    patient_date_of_birth = Column(Date)
    address_uid = Column(ForeignKey('public.address.uid', ondelete='SET NULL'))
    patient_date_of_death = Column(Date)
    patient_is_foetal_patient = Column(Boolean, nullable=False)
    patient_fetus_current_gestation = Column(Integer)
    patient_fetus_current_gestation_unit = Column(Text)
    patient_fetus_estimated_due_date = Column(Date)
    administrative_gender_cid = Column(ForeignKey('public.concept.uid'), nullable=False)
    ethnicity_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    life_status_cid = Column(ForeignKey('public.concept.uid'), nullable=False)
    patient_last_menstrual_period = Column(Date)
    additional_data = Column(JSONB(astext_type=Text()))
    karyotypic_sex_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    phenotypic_sex_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    patient_created_at = Column(Date)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    patient_human_readable_stored_id = Column(String, unique=True, server_default=text("patient_human_readable_id('patient_human_readable_id_sequence'::regclass)"))

    addres = relationship('Addres')
    concept = relationship('Concept', primaryjoin='Patient.administrative_gender_cid == Concept.uid')
    concept1 = relationship('Concept', primaryjoin='Patient.ethnicity_cid == Concept.uid')
    concept2 = relationship('Concept', primaryjoin='Patient.karyotypic_sex_cid == Concept.uid')
    concept3 = relationship('Concept', primaryjoin='Patient.life_status_cid == Concept.uid')
    person = relationship('Person')
    concept4 = relationship('Concept', primaryjoin='Patient.phenotypic_sex_cid == Concept.uid')


class Telecom(Base):
    __tablename__ = 'telecom'
    __table_args__ = {'schema': 'public'}

    person_uid = Column(ForeignKey('public.person.uid', ondelete='SET NULL'))
    telecom_value = Column(Text)
    telecom_rank = Column(Integer)
    system_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    use_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    person = relationship('Person')
    concept = relationship('Concept', primaryjoin='Telecom.system_cid == Concept.uid')
    concept1 = relationship('Concept', primaryjoin='Telecom.use_cid == Concept.uid')


class ClinicalEthnicity(Base):
    __tablename__ = 'clinical_ethnicity'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_uid = Column(ForeignKey('public.patient.uid'), nullable=False)
    clinical_ethnicity_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept')
    patient = relationship('Patient')


class Condition(Base):
    __tablename__ = 'condition'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    condition_clinical_status_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    condition_verification_status_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    condition_category_code_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    condition_certainty_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    condition_code_cid = Column(ForeignKey('public.concept.uid'), nullable=False)
    condition_body_site_code_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    patient_uid = Column(ForeignKey('public.patient.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept', primaryjoin='Condition.condition_body_site_code_cid == Concept.uid')
    concept1 = relationship('Concept', primaryjoin='Condition.condition_category_code_cid == Concept.uid')
    concept2 = relationship('Concept', primaryjoin='Condition.condition_certainty_cid == Concept.uid')
    concept3 = relationship('Concept', primaryjoin='Condition.condition_clinical_status_cid == Concept.uid')
    concept4 = relationship('Concept', primaryjoin='Condition.condition_code_cid == Concept.uid')
    concept5 = relationship('Concept', primaryjoin='Condition.condition_verification_status_cid == Concept.uid')
    patient = relationship('Patient')


class Contact(Base):
    __tablename__ = 'contact'
    __table_args__ = (
        UniqueConstraint('patient_uid', 'contact_person_uid'),
        {'schema': 'public'}
    )

    patient_uid = Column(ForeignKey('public.patient.uid'), nullable=False)
    contact_person_uid = Column(ForeignKey('public.person.uid'), nullable=False)
    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    relationship_type_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    person = relationship('Person')
    patient = relationship('Patient')
    concept = relationship('Concept')


class Observation(Base):
    __tablename__ = 'observation'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_uid = Column(ForeignKey('public.patient.uid'), nullable=False)
    observation_effective_from = Column(Date, nullable=False)
    observation_effective_to = Column(Date)
    observation_code_cid = Column(ForeignKey('public.concept.uid'), nullable=False)
    observation_value_code_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept', primaryjoin='Observation.observation_code_cid == Concept.uid')
    concept1 = relationship('Concept', primaryjoin='Observation.observation_value_code_cid == Concept.uid')
    patient = relationship('Patient')


class RelatedPerson(Base):
    __tablename__ = 'related_person'
    __table_args__ = {'schema': 'public'}

    source_patient_uid = Column(ForeignKey('public.patient.uid'), nullable=False)
    target_person_uid = Column(ForeignKey('public.person.uid'), nullable=False)
    relationship_type_cid = Column(ForeignKey('public.concept.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))

    concept = relationship('Concept')
    patient = relationship('Patient')
    person = relationship('Person')


class Tumour(Base):
    __tablename__ = 'tumour'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    _type_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    grade_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    parent_tumour_uid = Column(ForeignKey('public.tumour.uid', ondelete='SET NULL'))
    patient_uid = Column(ForeignKey('public.patient.uid'), nullable=False)
    presentation_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    prognostic_score_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    stage_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    additional_data = Column(JSONB(astext_type=Text()))
    clinician_uid = Column(ForeignKey('public.clinician.uid', ondelete='SET NULL'))
    organisation_uid = Column(UUID)
    tumour_diagnosis_day = Column(Text)
    tumour_diagnosis_month = Column(Text)
    tumour_diagnosis_year = Column(Text)
    diagnosis_age_in_years = Column(Integer)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept', primaryjoin='Tumour._type_cid == Concept.uid')
    clinician = relationship('Clinician')
    concept1 = relationship('Concept', primaryjoin='Tumour.grade_cid == Concept.uid')
    parent = relationship('Tumour', remote_side=[uid])
    patient = relationship('Patient')
    concept2 = relationship('Concept', primaryjoin='Tumour.presentation_cid == Concept.uid')
    concept3 = relationship('Concept', primaryjoin='Tumour.prognostic_score_cid == Concept.uid')
    concept4 = relationship('Concept', primaryjoin='Tumour.stage_cid == Concept.uid')


class ObservationComponent(Base):
    __tablename__ = 'observation_component'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    observation_uid = Column(ForeignKey('public.observation.uid'), nullable=False)
    observation_component_code_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    observation_component_value_string = Column(Text, nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept')
    observation = relationship('Observation')


class Referral(Base):
    __tablename__ = 'referral'
    __table_args__ = {'schema': 'public'}

    referral_occurrence_start = Column(Date)
    referral_is_prenatal_test = Column(Boolean)
    referral_expected_number_of_samples = Column(Integer)
    referral_date_last_submitted = Column(Date)
    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    parent_referral_uid = Column(ForeignKey('public.referral.uid', ondelete='SET NULL'))
    status_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    intent_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    priority_cid = Column(ForeignKey('public.concept.uid'), nullable=False)
    clinical_indication_uid = Column(UUID)
    reason_declined_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    ordering_entity_uid = Column(UUID)
    tumour_uid = Column(ForeignKey('public.tumour.uid', ondelete='SET NULL'))
    additional_data = Column(JSONB(astext_type=Text()))
    referral_notes = Column(Text)
    referral_created_at = Column(Date)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    referral_date_submitted = Column(Date)
    last_updated = Column(DateTime, index=True)
    referral_human_readable_stored_id = Column(String, unique=True, server_default=text("referral_human_readable_id('referral_human_readable_id_sequence'::regclass)"))
    responsible_clinician_uid = Column(ForeignKey('public.clinician.uid', ondelete='SET NULL'))

    concept = relationship('Concept', primaryjoin='Referral.intent_cid == Concept.uid')
    parent = relationship('Referral', remote_side=[uid])
    concept1 = relationship('Concept', primaryjoin='Referral.priority_cid == Concept.uid')
    concept2 = relationship('Concept', primaryjoin='Referral.reason_declined_cid == Concept.uid')
    clinician = relationship('Clinician')
    concept3 = relationship('Concept', primaryjoin='Referral.status_cid == Concept.uid')
    tumour = relationship('Tumour')


class TumourLabResult(Base):
    __tablename__ = 'tumour_lab_result'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    tumour_uid = Column(ForeignKey('public.tumour.uid'), nullable=False)
    flow_cytometry_result_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    immunohistochemistry_result_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    immunohistochemistry_results_percentage = Column(Integer)
    fish_target = Column(Text)
    fish_findings_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    fish_detected = Column(Boolean)
    number_cells_examined = Column(Integer)
    number_cells_detected_in = Column(Integer)
    number_copies_detected = Column(Integer)
    clinician_uid = Column(ForeignKey('public.clinician.uid', ondelete='SET NULL'))
    organisation_uid = Column(UUID)
    flow_cytometry_marker_name = Column(Text)
    immunohistochemistry_marker = Column(Text)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    clinician = relationship('Clinician')
    concept = relationship('Concept', primaryjoin='TumourLabResult.fish_findings_cid == Concept.uid')
    concept1 = relationship('Concept', primaryjoin='TumourLabResult.flow_cytometry_result_cid == Concept.uid')
    concept2 = relationship('Concept', primaryjoin='TumourLabResult.immunohistochemistry_result_cid == Concept.uid')
    tumour = relationship('Tumour')


class TumourMorphology(Base):
    __tablename__ = 'tumour_morphology'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    tumour_uid = Column(ForeignKey('public.tumour.uid'), nullable=False)
    morphology_cid = Column(ForeignKey('public.concept.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept')
    tumour = relationship('Tumour')


class TumourTopography(Base):
    __tablename__ = 'tumour_topography'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    tumour_uid = Column(ForeignKey('public.tumour.uid'), nullable=False)
    actual_body_site_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    primary_body_site_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept', primaryjoin='TumourTopography.actual_body_site_cid == Concept.uid')
    concept1 = relationship('Concept', primaryjoin='TumourTopography.primary_body_site_cid == Concept.uid')
    tumour = relationship('Tumour')


class ReferralAdditionalClinician(Base):
    __tablename__ = 'referral_additional_clinician'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_uid = Column(ForeignKey('public.referral.uid'), nullable=False)
    clinician_uid = Column(ForeignKey('public.clinician.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    clinician = relationship('Clinician')
    referral = relationship('Referral')


class ReferralAttachment(Base):
    __tablename__ = 'referral_attachment'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_uid = Column(ForeignKey('public.referral.uid'), nullable=False)
    attachment_uid = Column(ForeignKey('public.attachment.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    attachment = relationship('Attachment')
    referral = relationship('Referral')


class ReferralParticipant(Base):
    __tablename__ = 'referral_participant'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_uid = Column(ForeignKey('public.referral.uid'), nullable=False)
    patient_uid = Column(ForeignKey('public.patient.uid'), nullable=False)
    referral_participant_is_proband = Column(Boolean, nullable=False)
    additional_data = Column(JSONB(astext_type=Text()))
    consanguinity_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    disease_status_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    father_affected_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    mother_affected_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    referral_participant_age_at_onset = Column(Integer)
    referral_participant_full_brother_count = Column(Integer)
    referral_participant_full_brothers_affected = Column(Integer)
    referral_participant_full_sister_count = Column(Integer)
    referral_participant_full_sisters_affected = Column(Integer)
    referral_participant_other_relationship_details = Column(Text)
    relationship_to_proband_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept', primaryjoin='ReferralParticipant.consanguinity_cid == Concept.uid')
    concept1 = relationship('Concept', primaryjoin='ReferralParticipant.disease_status_cid == Concept.uid')
    concept2 = relationship('Concept', primaryjoin='ReferralParticipant.father_affected_cid == Concept.uid')
    concept3 = relationship('Concept', primaryjoin='ReferralParticipant.mother_affected_cid == Concept.uid')
    patient = relationship('Patient')
    referral = relationship('Referral')
    concept4 = relationship('Concept', primaryjoin='ReferralParticipant.relationship_to_proband_cid == Concept.uid')


class ReferralTest(Base):
    __tablename__ = 'referral_test'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_test_expected_number_of_patients = Column(Integer)
    ci_test_type_uid = Column(UUID)
    referral_uid = Column(ForeignKey('public.referral.uid', ondelete='SET NULL'))
    penetrance_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    referral_test_medical_review_qc_state_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    status_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    additional_data = Column(JSONB(astext_type=Text()))
    interpretation_lab_uid = Column(UUID)
    sample_processing_lab_uid = Column(UUID)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept', primaryjoin='ReferralTest.penetrance_cid == Concept.uid')
    concept1 = relationship('Concept', primaryjoin='ReferralTest.referral_test_medical_review_qc_state_cid == Concept.uid')
    referral = relationship('Referral')
    concept2 = relationship('Concept', primaryjoin='ReferralTest.status_cid == Concept.uid')


class Sample(Base):
    __tablename__ = 'sample'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    body_site_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    other_referral_request_uid = Column(ForeignKey('public.referral.uid', ondelete='SET NULL'))
    parent_uid = Column(ForeignKey('public.sample.uid', ondelete='SET NULL'))
    patient_uid = Column(ForeignKey('public.patient.uid'), nullable=False)
    percentage_of_malignant_cells = Column(Integer)
    sample_morphology_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    sample_number_of_slides = Column(Integer)
    sample_ready_for_dispatch = Column(Boolean)
    sample_requested_for_other_test = Column(Boolean)
    sample_shipping_status_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    sample_state_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    sample_topography_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    sample_type_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    tumour_uid = Column(ForeignKey('public.tumour.uid', ondelete='SET NULL'))
    additional_data = Column(JSONB(astext_type=Text()))
    sample_collection_date = Column(DateTime)
    sample_notes = Column(Text)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept', primaryjoin='Sample.body_site_cid == Concept.uid')
    referral = relationship('Referral')
    parent = relationship('Sample', remote_side=[uid])
    patient = relationship('Patient')
    concept1 = relationship('Concept', primaryjoin='Sample.sample_morphology_cid == Concept.uid')
    concept2 = relationship('Concept', primaryjoin='Sample.sample_shipping_status_cid == Concept.uid')
    concept3 = relationship('Concept', primaryjoin='Sample.sample_state_cid == Concept.uid')
    concept4 = relationship('Concept', primaryjoin='Sample.sample_topography_cid == Concept.uid')
    concept5 = relationship('Concept', primaryjoin='Sample.sample_type_cid == Concept.uid')
    tumour = relationship('Tumour')


class TumourDescription(Base):
    __tablename__ = 'tumour_description'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    tumour_uid = Column(ForeignKey('public.tumour.uid'), nullable=False)
    tumour_description = Column(Text, nullable=False)
    referral_uid = Column(ForeignKey('public.referral.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    referral = relationship('Referral')
    tumour = relationship('Tumour')


class Identifier(Base):
    __tablename__ = 'identifier'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    value = Column(Text)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    organisation_uid = Column(UUID)
    condition_uid = Column(ForeignKey('public.condition.uid', ondelete='SET NULL'))
    observation_uid = Column(ForeignKey('public.observation.uid', ondelete='SET NULL'))
    patient_uid = Column(ForeignKey('public.patient.uid', ondelete='SET NULL'))
    polymorphic_type = Column(Text)
    referral_uid = Column(ForeignKey('public.referral.uid', ondelete='SET NULL'))
    sample_uid = Column(ForeignKey('public.sample.uid', ondelete='SET NULL'))
    tumour_uid = Column(ForeignKey('public.tumour.uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    type_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))

    condition = relationship('Condition')
    observation = relationship('Observation')
    patient = relationship('Patient')
    referral = relationship('Referral')
    sample = relationship('Sample')
    tumour = relationship('Tumour')
    concept = relationship('Concept')


class ProcedureRequest(Base):
    __tablename__ = 'procedure_request'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_test_uid = Column(ForeignKey('public.referral_test.uid', ondelete='SET NULL'))
    referral_participant_uid = Column(ForeignKey('public.referral_participant.uid'), nullable=False)
    additional_data = Column(JSONB(astext_type=Text()))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    referral_participant = relationship('ReferralParticipant')
    referral_test = relationship('ReferralTest')


class ReferralPanel(Base):
    __tablename__ = 'referral_panel'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_test_uid = Column(ForeignKey('public.referral_test.uid', ondelete='CASCADE'), nullable=False)
    referral_panel_id = Column(Text)
    referral_panel_display = Column(Text)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    referral_test = relationship('ReferralTest')


class ReferralParticipantAttachment(Base):
    __tablename__ = 'referral_participant_attachment'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_participant_uid = Column(ForeignKey('public.referral_participant.uid'), nullable=False)
    attachment_uid = Column(ForeignKey('public.attachment.uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    attachment = relationship('Attachment')
    referral_participant = relationship('ReferralParticipant')


class ReferralSample(Base):
    __tablename__ = 'referral_sample'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    sample_uid = Column(ForeignKey('public.sample.uid'), nullable=False)
    referral_uid = Column(ForeignKey('public.referral.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    referral = relationship('Referral')
    sample = relationship('Sample')


class ReferralTestTargetRegion(Base):
    __tablename__ = 'referral_test_target_region'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_test_uid = Column(ForeignKey('public.referral_test.uid', ondelete='CASCADE'), nullable=False)
    referral_test_target_region = Column(Text, nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    referral_test = relationship('ReferralTest')


class ReferralTestTargetVariant(Base):
    __tablename__ = 'referral_test_target_variant'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_test_uid = Column(ForeignKey('public.referral_test.uid', ondelete='CASCADE'), nullable=False)
    referral_test_target_variant = Column(Text, nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    referral_test = relationship('ReferralTest')


class Consent(Base):
    __tablename__ = 'consent'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_uid = Column(ForeignKey('public.patient.uid'), nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.uid', ondelete='SET NULL'))
    status_cid = Column(ForeignKey('public.concept.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    identifier = relationship('Identifier')
    patient = relationship('Patient')
    concept = relationship('Concept')


class ConsentQuestionnaire(Base):
    __tablename__ = 'consent_questionnaire'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    identifier_uid = Column(ForeignKey('public.identifier.uid'), nullable=False)
    version = Column(Text)
    name = Column(Text)
    title = Column(Text)
    status_cid = Column(ForeignKey('public.concept.uid'), nullable=False)
    changed = Column(DateTime)
    description = Column(Text)
    purpose = Column(Text)
    approval_date = Column(DateTime)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    identifier = relationship('Identifier')
    concept = relationship('Concept')


class ConsentDocumentReference(Base):
    __tablename__ = 'consent_document_reference'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(ForeignKey('public.consent.uid', ondelete='SET NULL'))
    identifier_uid = Column(ForeignKey('public.identifier.uid', ondelete='SET NULL'))
    status_cid = Column(ForeignKey('public.concept.uid'), nullable=False)
    indexed = Column(DateTime, nullable=False)
    description = Column(Text)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent = relationship('Consent')
    identifier = relationship('Identifier')
    concept = relationship('Concept')


class ConsentNote(Base):
    __tablename__ = 'consent_note'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(ForeignKey('public.consent.uid'), nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.uid'), nullable=False)
    consent_note_text = Column(Text, nullable=False)
    consent_note_time = Column(DateTime)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent = relationship('Consent')
    identifier = relationship('Identifier')


class ConsentOrganisation(Base):
    __tablename__ = 'consent_organisation'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(ForeignKey('public.consent.uid'), nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent = relationship('Consent')
    identifier = relationship('Identifier')


class ConsentQuestionnaireResponse(Base):
    __tablename__ = 'consent_questionnaire_response'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(ForeignKey('public.consent.uid', ondelete='SET NULL'))
    identifier_uid = Column(ForeignKey('public.identifier.uid', ondelete='SET NULL'))
    status_cid = Column(ForeignKey('public.concept.uid'), nullable=False)
    consent_questionnaire_response_authored = Column(DateTime, nullable=False)
    source_identifier_uid = Column(ForeignKey('public.identifier.uid'), nullable=False)
    consent_questionnaire_uid = Column(ForeignKey('public.consent_questionnaire.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent_questionnaire = relationship('ConsentQuestionnaire')
    consent = relationship('Consent')
    identifier = relationship('Identifier', primaryjoin='ConsentQuestionnaireResponse.identifier_uid == Identifier.uid')
    identifier1 = relationship('Identifier', primaryjoin='ConsentQuestionnaireResponse.source_identifier_uid == Identifier.uid')
    concept = relationship('Concept')


class ConsentWitnes(Base):
    __tablename__ = 'consent_witness'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(ForeignKey('public.consent.uid'), nullable=False)
    consent_witness_url = Column(Text, nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent = relationship('Consent')
    identifier = relationship('Identifier')


class ConsentingParty(Base):
    __tablename__ = 'consenting_party'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    identifier_uid = Column(ForeignKey('public.identifier.uid'), nullable=False)
    relationship_cid = Column(ForeignKey('public.concept.uid', ondelete='SET NULL'))
    consent_uid = Column(ForeignKey('public.consent.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent = relationship('Consent')
    identifier = relationship('Identifier')
    concept = relationship('Concept')


class CqItem(Base):
    __tablename__ = 'cq_item'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_questionnaire_uid = Column(ForeignKey('public.consent_questionnaire.uid'), nullable=False)
    cq_item_link_id = Column(Text, nullable=False)
    cq_item_prefix = Column(Text)
    cq_item_text = Column(Text)
    cq_item_required = Column(Boolean)
    cq_item_read_only = Column(Boolean)
    cq_item_max_length = Column(Integer)
    cq_parent_item_uid = Column(ForeignKey('public.cq_item.uid', ondelete='SET NULL'))
    cq_item_initial_bool = Column(Boolean)
    cq_item_initial_integer = Column(Integer)
    cq_item_initial_string = Column(Text)
    cq_item_initial_decimal = Column(Numeric)
    cq_item_initial_date = Column(Date)
    cq_item_initial_datetime = Column(DateTime)
    cq_item_initial_time = Column(Time)
    initial_attachment_uid = Column(ForeignKey('public.attachment.uid', ondelete='SET NULL'))
    cq_item_type_cid = Column(ForeignKey('public.concept.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent_questionnaire = relationship('ConsentQuestionnaire')
    concept = relationship('Concept')
    parent = relationship('CqItem', remote_side=[uid])
    attachment = relationship('Attachment')


class OrganisationConsent(Base):
    __tablename__ = 'organisation_consent'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    organisation_uid = Column(UUID, nullable=False)
    consent_uid = Column(ForeignKey('public.consent.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent = relationship('Consent')


class CdrAuthor(Base):
    __tablename__ = 'cdr_author'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_document_reference_uid = Column(ForeignKey('public.consent_document_reference.uid'), nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.uid'), nullable=False)
    cdr_author_type_cid = Column(ForeignKey('public.concept.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept')
    consent_document_reference = relationship('ConsentDocumentReference')
    identifier = relationship('Identifier')


class CdrContent(Base):
    __tablename__ = 'cdr_content'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_document_reference_uid = Column(ForeignKey('public.consent_document_reference.uid'), nullable=False)
    attachment_uid = Column(ForeignKey('public.attachment.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    attachment = relationship('Attachment')
    consent_document_reference = relationship('ConsentDocumentReference')


class CdrRelatesTo(Base):
    __tablename__ = 'cdr_relates_to'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    code_cid = Column(ForeignKey('public.concept.uid'), nullable=False)
    consent_document_reference_uid = Column(ForeignKey('public.consent_document_reference.uid'), nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept')
    consent_document_reference = relationship('ConsentDocumentReference')
    identifier = relationship('Identifier')


class CqItemEnableWhen(Base):
    __tablename__ = 'cq_item_enable_when'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    cq_item_uid = Column(ForeignKey('public.cq_item.uid', ondelete='SET NULL'))
    cq_item_enable_when_question = Column(Text, nullable=False)
    cq_item_enable_when_has_answer = Column(Boolean)
    cq_item_enable_when_answer_bool = Column(Boolean)
    cq_item_enable_when_answer_integer = Column(Integer)
    cq_item_enable_when_answer_decimal = Column(Numeric)
    cq_item_enable_when_answer_string = Column(Text)
    cq_item_enable_when_answer_date = Column(Date)
    cq_item_enable_when_answer_datetime = Column(DateTime)
    cq_item_enable_when_answer_time = Column(Time)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    cq_item = relationship('CqItem')


class CqItemOption(Base):
    __tablename__ = 'cq_item_option'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    cq_item_uid = Column(ForeignKey('public.cq_item.uid'), nullable=False)
    cq_item_option_value_integer = Column(Integer)
    cq_item_option_value_string = Column(Text)
    cq_item_option_value_date = Column(Date)
    cq_item_option_value_time = Column(Time)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    cq_item = relationship('CqItem')


class CqrAuthor(Base):
    __tablename__ = 'cqr_author'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_questionnaire_response_uid = Column(ForeignKey('public.consent_questionnaire_response.uid'), nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.uid'), nullable=False)
    author_type_cid = Column(ForeignKey('public.concept.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept')
    consent_questionnaire_response = relationship('ConsentQuestionnaireResponse')
    identifier = relationship('Identifier')


class CqrBasedOn(Base):
    __tablename__ = 'cqr_based_on'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_questionnaire_response_uid = Column(ForeignKey('public.consent_questionnaire_response.uid'), nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent_questionnaire_response = relationship('ConsentQuestionnaireResponse')
    identifier = relationship('Identifier')


class CqrItem(Base):
    __tablename__ = 'cqr_item'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_questionnaire_response_uid = Column(ForeignKey('public.consent_questionnaire_response.uid', ondelete='CASCADE'), nullable=False)
    cqr_item_link_id = Column(Text, nullable=False)
    cqr_item_text = Column(Text, nullable=False)
    subject_identifier_uid = Column(ForeignKey('public.identifier.uid'), nullable=False)
    cqr_parent_item_uid = Column(ForeignKey('public.cqr_item.uid', ondelete='SET NULL'), index=True)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent_questionnaire_response = relationship('ConsentQuestionnaireResponse')
    parent = relationship('CqrItem', remote_side=[uid])
    identifier = relationship('Identifier')


class CqrAnswer(Base):
    __tablename__ = 'cqr_answer'
    __table_args__ = {'schema': 'public'}

    uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    cqr_item_uid = Column(ForeignKey('public.cqr_item.uid', ondelete='CASCADE'), nullable=False, index=True)
    value_bool = Column(Boolean)
    value_decimal = Column(Numeric)
    value_integer = Column(Integer)
    value_date = Column(Date)
    value_datetime = Column(DateTime)
    value_time = Column(Time)
    value_string = Column(Text)
    value_attachment_uid = Column(ForeignKey('public.attachment.uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    cqr_item = relationship('CqrItem')
    attachment = relationship('Attachment')
