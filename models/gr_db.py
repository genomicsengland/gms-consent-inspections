# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKey, Integer, LargeBinary, Numeric, String, Table, Text, Time, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Addres(Base):
    __tablename__ = 'address'
    __table_args__ = {'schema': 'public'}

    address_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
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


class Codesystem(Base):
    __tablename__ = 'codesystem'
    __table_args__ = {'schema': 'public'}

    codesystem_uri = Column(String(255), primary_key=True)
    codesystem_version = Column(Text)
    codesystem_name = Column(Text)


t_db_version = Table(
    'db_version', metadata,
    Column('version', Text),
    schema='public'
)


t_mi_referral = Table(
    'mi_referral', metadata,
    Column('referral_uid', UUID),
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


class SequenceStatu(Base):
    __tablename__ = 'sequence_status'
    __table_args__ = {'schema': 'public'}

    sequence_status_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    sequence_status_name = Column(String(255), nullable=False, unique=True)
    sequence_status_last_reset = Column(DateTime, nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)


class Technology(Base):
    __tablename__ = 'technology'
    __table_args__ = {'schema': 'public'}

    technology_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))


class Concept(Base):
    __tablename__ = 'concept'
    __table_args__ = (
        UniqueConstraint('concept_code', 'codesystem_uri'),
        {'schema': 'public'}
    )

    concept_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    concept_code = Column(Text, nullable=False)
    concept_display = Column(Text, nullable=False)
    codesystem_uri = Column(ForeignKey('public.codesystem.codesystem_uri'), nullable=False)
    concept_sort_order = Column(Integer, nullable=False, server_default=text("0"))

    codesystem = relationship('Codesystem')


class Person(Base):
    __tablename__ = 'person'
    __table_args__ = {'schema': 'public'}

    person_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    address_uid = Column(ForeignKey('public.address.address_uid', ondelete='SET NULL'))
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

    attachment_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    attachment_content_type = Column(Text)
    attachment_data = Column(LargeBinary)
    attachment_url = Column(Text)
    attachment_size = Column(Integer)
    attachment_hash = Column(LargeBinary)
    attachment_title = Column(Text)
    attachment_created = Column(DateTime)
    attachment_type_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept')


class Clinician(Base):
    __tablename__ = 'clinician'
    __table_args__ = {'schema': 'public'}

    clinician_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    clinician_forename = Column(Text)
    clinician_surname = Column(Text, nullable=False)
    clinician_departmental_address = Column(Text)
    clinician_profession_registration_number = Column(Text)
    role_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    clinician_email_address = Column(String(255))
    clinician_phone_number = Column(Text)
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept')


class Patient(Base):
    __tablename__ = 'patient'
    __table_args__ = {'schema': 'public'}

    patient_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    person_uid = Column(ForeignKey('public.person.person_uid'), nullable=False)
    patient_date_of_birth = Column(Date)
    address_uid = Column(ForeignKey('public.address.address_uid', ondelete='SET NULL'))
    patient_date_of_death = Column(Date)
    patient_is_foetal_patient = Column(Boolean, nullable=False)
    patient_fetus_current_gestation = Column(Integer)
    patient_fetus_current_gestation_unit = Column(Text)
    patient_fetus_estimated_due_date = Column(Date)
    administrative_gender_cid = Column(ForeignKey('public.concept.concept_uid'), nullable=False)
    ethnicity_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    life_status_cid = Column(ForeignKey('public.concept.concept_uid'), nullable=False)
    patient_last_menstrual_period = Column(Date)
    additional_data = Column(JSONB(astext_type=Text()))
    karyotypic_sex_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    phenotypic_sex_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    patient_created_at = Column(Date)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    patient_human_readable_stored_id = Column(String, unique=True, server_default=text("patient_human_readable_id('patient_human_readable_id_sequence'::regclass)"))

    addres = relationship('Addres')
    concept = relationship('Concept', primaryjoin='Patient.administrative_gender_cid == Concept.concept_uid')
    concept1 = relationship('Concept', primaryjoin='Patient.ethnicity_cid == Concept.concept_uid')
    concept2 = relationship('Concept', primaryjoin='Patient.karyotypic_sex_cid == Concept.concept_uid')
    concept3 = relationship('Concept', primaryjoin='Patient.life_status_cid == Concept.concept_uid')
    person = relationship('Person')
    concept4 = relationship('Concept', primaryjoin='Patient.phenotypic_sex_cid == Concept.concept_uid')


class Telecom(Base):
    __tablename__ = 'telecom'
    __table_args__ = {'schema': 'public'}

    person_uid = Column(ForeignKey('public.person.person_uid', ondelete='SET NULL'))
    telecom_value = Column(Text)
    telecom_rank = Column(Integer)
    system_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    telecom_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    use_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    person = relationship('Person')
    concept = relationship('Concept', primaryjoin='Telecom.system_cid == Concept.concept_uid')
    concept1 = relationship('Concept', primaryjoin='Telecom.use_cid == Concept.concept_uid')


class ClinicalEthnicity(Base):
    __tablename__ = 'clinical_ethnicity'
    __table_args__ = {'schema': 'public'}

    clinical_ethnicity_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_uid = Column(ForeignKey('public.patient.patient_uid'), nullable=False)
    clinical_ethnicity_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept')
    patient = relationship('Patient')


class Condition(Base):
    __tablename__ = 'condition'
    __table_args__ = {'schema': 'public'}

    condition_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    condition_clinical_status_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    condition_verification_status_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    condition_category_code_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    condition_certainty_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    condition_code_cid = Column(ForeignKey('public.concept.concept_uid'), nullable=False)
    condition_body_site_code_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    patient_uid = Column(ForeignKey('public.patient.patient_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept', primaryjoin='Condition.condition_body_site_code_cid == Concept.concept_uid')
    concept1 = relationship('Concept', primaryjoin='Condition.condition_category_code_cid == Concept.concept_uid')
    concept2 = relationship('Concept', primaryjoin='Condition.condition_certainty_cid == Concept.concept_uid')
    concept3 = relationship('Concept', primaryjoin='Condition.condition_clinical_status_cid == Concept.concept_uid')
    concept4 = relationship('Concept', primaryjoin='Condition.condition_code_cid == Concept.concept_uid')
    concept5 = relationship('Concept', primaryjoin='Condition.condition_verification_status_cid == Concept.concept_uid')
    patient = relationship('Patient')


t_contact = Table(
    'contact', metadata,
    Column('patient_uid', ForeignKey('public.patient.patient_uid'), nullable=False),
    Column('contact_person_uid', ForeignKey('public.person.person_uid'), nullable=False),
    Column('contact_uid', UUID, nullable=False, server_default=text("uuid_generate_v4()")),
    Column('relationship_type_cid', ForeignKey('public.concept.concept_uid', ondelete='SET NULL')),
    Column('last_updated_by', String(255)),
    Column('last_updated_by_session', String(255)),
    Column('last_updated', DateTime, index=True),
    UniqueConstraint('patient_uid', 'contact_person_uid'),
    schema='public'
)


class Observation(Base):
    __tablename__ = 'observation'
    __table_args__ = {'schema': 'public'}

    observation_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_uid = Column(ForeignKey('public.patient.patient_uid'), nullable=False)
    observation_effective_from = Column(Date, nullable=False)
    observation_effective_to = Column(Date)
    observation_code_cid = Column(ForeignKey('public.concept.concept_uid'), nullable=False)
    observation_value_code_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept', primaryjoin='Observation.observation_code_cid == Concept.concept_uid')
    concept1 = relationship('Concept', primaryjoin='Observation.observation_value_code_cid == Concept.concept_uid')
    patient = relationship('Patient')


class RelatedPerson(Base):
    __tablename__ = 'related_person'
    __table_args__ = {'schema': 'public'}

    source_patient_uid = Column(ForeignKey('public.patient.patient_uid'), primary_key=True, nullable=False)
    target_person_uid = Column(ForeignKey('public.person.person_uid'), primary_key=True, nullable=False)
    relationship_type_cid = Column(ForeignKey('public.concept.concept_uid'), primary_key=True, nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)
    related_person_uid = Column(UUID, nullable=False, server_default=text("uuid_generate_v4()"))

    concept = relationship('Concept')
    patient = relationship('Patient')
    person = relationship('Person')


class Tumour(Base):
    __tablename__ = 'tumour'
    __table_args__ = {'schema': 'public'}

    tumour_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    _type_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    grade_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    parent_tumour_uid = Column(ForeignKey('public.tumour.tumour_uid', ondelete='SET NULL'))
    patient_uid = Column(ForeignKey('public.patient.patient_uid'), nullable=False)
    presentation_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    prognostic_score_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    stage_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    additional_data = Column(JSONB(astext_type=Text()))
    clinician_uid = Column(ForeignKey('public.clinician.clinician_uid', ondelete='SET NULL'))
    organisation_uid = Column(UUID)
    tumour_diagnosis_day = Column(Text)
    tumour_diagnosis_month = Column(Text)
    tumour_diagnosis_year = Column(Text)
    diagnosis_age_in_years = Column(Integer)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept', primaryjoin='Tumour._type_cid == Concept.concept_uid')
    clinician = relationship('Clinician')
    concept1 = relationship('Concept', primaryjoin='Tumour.grade_cid == Concept.concept_uid')
    parent = relationship('Tumour', remote_side=[tumour_uid])
    patient = relationship('Patient')
    concept2 = relationship('Concept', primaryjoin='Tumour.presentation_cid == Concept.concept_uid')
    concept3 = relationship('Concept', primaryjoin='Tumour.prognostic_score_cid == Concept.concept_uid')
    concept4 = relationship('Concept', primaryjoin='Tumour.stage_cid == Concept.concept_uid')


class ObservationComponent(Base):
    __tablename__ = 'observation_component'
    __table_args__ = {'schema': 'public'}

    observation_component_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    observation_uid = Column(ForeignKey('public.observation.observation_uid'), nullable=False)
    observation_component_code_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
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
    referral_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    parent_referral_uid = Column(ForeignKey('public.referral.referral_uid', ondelete='SET NULL'))
    status_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    intent_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    priority_cid = Column(ForeignKey('public.concept.concept_uid'), nullable=False)
    clinical_indication_uid = Column(UUID)
    reason_declined_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    ordering_entity_uid = Column(UUID)
    tumour_uid = Column(ForeignKey('public.tumour.tumour_uid', ondelete='SET NULL'))
    additional_data = Column(JSONB(astext_type=Text()))
    referral_notes = Column(Text)
    referral_created_at = Column(Date)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    referral_date_submitted = Column(Date)
    last_updated = Column(DateTime, index=True)
    referral_human_readable_stored_id = Column(String, unique=True, server_default=text("referral_human_readable_id('referral_human_readable_id_sequence'::regclass)"))

    concept = relationship('Concept', primaryjoin='Referral.intent_cid == Concept.concept_uid')
    parent = relationship('Referral', remote_side=[referral_uid])
    concept1 = relationship('Concept', primaryjoin='Referral.priority_cid == Concept.concept_uid')
    concept2 = relationship('Concept', primaryjoin='Referral.reason_declined_cid == Concept.concept_uid')
    concept3 = relationship('Concept', primaryjoin='Referral.status_cid == Concept.concept_uid')
    tumour = relationship('Tumour')


class TumourLabResult(Base):
    __tablename__ = 'tumour_lab_result'
    __table_args__ = {'schema': 'public'}

    tumour_lab_result_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    tumour_uid = Column(ForeignKey('public.tumour.tumour_uid'), nullable=False)
    flow_cytometry_result_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    immunohistochemistry_result_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    immunohistochemistry_results_percentage = Column(Integer)
    fish_target = Column(Text)
    fish_findings_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    fish_detected = Column(Boolean)
    number_cells_examined = Column(Integer)
    number_cells_detected_in = Column(Integer)
    number_copies_detected = Column(Integer)
    clinician_uid = Column(ForeignKey('public.clinician.clinician_uid', ondelete='SET NULL'))
    organisation_uid = Column(UUID)
    flow_cytometry_marker_name = Column(Text)
    immunohistochemistry_marker = Column(Text)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    clinician = relationship('Clinician')
    concept = relationship('Concept', primaryjoin='TumourLabResult.fish_findings_cid == Concept.concept_uid')
    concept1 = relationship('Concept', primaryjoin='TumourLabResult.flow_cytometry_result_cid == Concept.concept_uid')
    concept2 = relationship('Concept', primaryjoin='TumourLabResult.immunohistochemistry_result_cid == Concept.concept_uid')
    tumour = relationship('Tumour')


class TumourMorphology(Base):
    __tablename__ = 'tumour_morphology'
    __table_args__ = {'schema': 'public'}

    tumour_morphology_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    tumour_uid = Column(ForeignKey('public.tumour.tumour_uid'), nullable=False)
    morphology_cid = Column(ForeignKey('public.concept.concept_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept')
    tumour = relationship('Tumour')


class TumourTopography(Base):
    __tablename__ = 'tumour_topography'
    __table_args__ = {'schema': 'public'}

    tumour_topography_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    tumour_uid = Column(ForeignKey('public.tumour.tumour_uid'), nullable=False)
    actual_body_site_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    primary_body_site_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept', primaryjoin='TumourTopography.actual_body_site_cid == Concept.concept_uid')
    concept1 = relationship('Concept', primaryjoin='TumourTopography.primary_body_site_cid == Concept.concept_uid')
    tumour = relationship('Tumour')


class ReferralAttachment(Base):
    __tablename__ = 'referral_attachment'
    __table_args__ = {'schema': 'public'}

    referral_attachment_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_uid = Column(ForeignKey('public.referral.referral_uid'), nullable=False)
    attachment_uid = Column(ForeignKey('public.attachment.attachment_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    attachment = relationship('Attachment')
    referral = relationship('Referral')


class ReferralClinician(Base):
    __tablename__ = 'referral_clinician'
    __table_args__ = {'schema': 'public'}

    referral_clinician_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_uid = Column(ForeignKey('public.referral.referral_uid'), nullable=False)
    clinician_uid = Column(ForeignKey('public.clinician.clinician_uid'), nullable=False)
    referral_clinician_role_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    organisation_uid = Column(UUID)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    clinician = relationship('Clinician')
    concept = relationship('Concept')
    referral = relationship('Referral')


class ReferralParticipant(Base):
    __tablename__ = 'referral_participant'
    __table_args__ = {'schema': 'public'}

    referral_participant_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_uid = Column(ForeignKey('public.referral.referral_uid'), nullable=False)
    patient_uid = Column(ForeignKey('public.patient.patient_uid'), nullable=False)
    referral_participant_is_proband = Column(Boolean, nullable=False)
    additional_data = Column(JSONB(astext_type=Text()))
    consanguinity_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    disease_status_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    father_affected_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    mother_affected_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    referral_participant_age_at_onset = Column(Integer)
    referral_participant_full_brother_count = Column(Integer)
    referral_participant_full_brothers_affected = Column(Integer)
    referral_participant_full_sister_count = Column(Integer)
    referral_participant_full_sisters_affected = Column(Integer)
    referral_participant_other_relationship_details = Column(Text)
    relationship_to_proband_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept', primaryjoin='ReferralParticipant.consanguinity_cid == Concept.concept_uid')
    concept1 = relationship('Concept', primaryjoin='ReferralParticipant.disease_status_cid == Concept.concept_uid')
    concept2 = relationship('Concept', primaryjoin='ReferralParticipant.father_affected_cid == Concept.concept_uid')
    concept3 = relationship('Concept', primaryjoin='ReferralParticipant.mother_affected_cid == Concept.concept_uid')
    patient = relationship('Patient')
    referral = relationship('Referral')
    concept4 = relationship('Concept', primaryjoin='ReferralParticipant.relationship_to_proband_cid == Concept.concept_uid')


class ReferralTest(Base):
    __tablename__ = 'referral_test'
    __table_args__ = {'schema': 'public'}

    referral_test_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_test_expected_number_of_patients = Column(Integer)
    ci_test_type_uid = Column(UUID)
    referral_uid = Column(ForeignKey('public.referral.referral_uid', ondelete='SET NULL'))
    penetrance_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    referral_test_medical_review_qc_state_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    status_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    additional_data = Column(JSONB(astext_type=Text()))
    interpretation_lab_uid = Column(UUID)
    sample_processing_lab_uid = Column(UUID)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept', primaryjoin='ReferralTest.penetrance_cid == Concept.concept_uid')
    concept1 = relationship('Concept', primaryjoin='ReferralTest.referral_test_medical_review_qc_state_cid == Concept.concept_uid')
    referral = relationship('Referral')
    concept2 = relationship('Concept', primaryjoin='ReferralTest.status_cid == Concept.concept_uid')


class Sample(Base):
    __tablename__ = 'sample'
    __table_args__ = {'schema': 'public'}

    sample_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    body_site_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    other_referral_request_uid = Column(ForeignKey('public.referral.referral_uid', ondelete='SET NULL'))
    parent_uid = Column(ForeignKey('public.sample.sample_uid', ondelete='SET NULL'))
    patient_uid = Column(ForeignKey('public.patient.patient_uid'), nullable=False)
    percentage_of_malignant_cells = Column(Integer)
    sample_morphology_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    sample_number_of_slides = Column(Integer)
    sample_ready_for_dispatch = Column(Boolean)
    sample_requested_for_other_test = Column(Boolean)
    sample_shipping_status_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    sample_state_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    sample_topography_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    sample_type_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    tumour_uid = Column(ForeignKey('public.tumour.tumour_uid', ondelete='SET NULL'))
    additional_data = Column(JSONB(astext_type=Text()))
    sample_collection_date = Column(DateTime)
    sample_notes = Column(Text)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept', primaryjoin='Sample.body_site_cid == Concept.concept_uid')
    referral = relationship('Referral')
    parent = relationship('Sample', remote_side=[sample_uid])
    patient = relationship('Patient')
    concept1 = relationship('Concept', primaryjoin='Sample.sample_morphology_cid == Concept.concept_uid')
    concept2 = relationship('Concept', primaryjoin='Sample.sample_shipping_status_cid == Concept.concept_uid')
    concept3 = relationship('Concept', primaryjoin='Sample.sample_state_cid == Concept.concept_uid')
    concept4 = relationship('Concept', primaryjoin='Sample.sample_topography_cid == Concept.concept_uid')
    concept5 = relationship('Concept', primaryjoin='Sample.sample_type_cid == Concept.concept_uid')
    tumour = relationship('Tumour')


class TumourDescription(Base):
    __tablename__ = 'tumour_description'
    __table_args__ = {'schema': 'public'}

    tumour_description_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    tumour_uid = Column(ForeignKey('public.tumour.tumour_uid'), nullable=False)
    tumour_description = Column(Text, nullable=False)
    referral_uid = Column(ForeignKey('public.referral.referral_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    referral = relationship('Referral')
    tumour = relationship('Tumour')


class Identifier(Base):
    __tablename__ = 'identifier'
    __table_args__ = {'schema': 'public'}

    identifier_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    value = Column(Text)
    concept_uid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    organisation_uid = Column(UUID)
    condition_uid = Column(ForeignKey('public.condition.condition_uid', ondelete='SET NULL'))
    observation_uid = Column(ForeignKey('public.observation.observation_uid', ondelete='SET NULL'))
    patient_uid = Column(ForeignKey('public.patient.patient_uid', ondelete='SET NULL'))
    polymorphic_type = Column(Text)
    referral_uid = Column(ForeignKey('public.referral.referral_uid', ondelete='SET NULL'))
    sample_uid = Column(ForeignKey('public.sample.sample_uid', ondelete='SET NULL'))
    tumour_uid = Column(ForeignKey('public.tumour.tumour_uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept')
    condition = relationship('Condition')
    observation = relationship('Observation')
    patient = relationship('Patient')
    referral = relationship('Referral')
    sample = relationship('Sample')
    tumour = relationship('Tumour')


class ProcedureRequest(Base):
    __tablename__ = 'procedure_request'
    __table_args__ = {'schema': 'public'}

    procedure_request_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_test_uid = Column(ForeignKey('public.referral_test.referral_test_uid', ondelete='SET NULL'))
    referral_participant_uid = Column(ForeignKey('public.referral_participant.referral_participant_uid'), nullable=False)
    additional_data = Column(JSONB(astext_type=Text()))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    referral_participant = relationship('ReferralParticipant')
    referral_test = relationship('ReferralTest')


class ReferralPanel(Base):
    __tablename__ = 'referral_panel'
    __table_args__ = {'schema': 'public'}

    referral_panel_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_test_uid = Column(ForeignKey('public.referral_test.referral_test_uid', ondelete='CASCADE'), nullable=False)
    referral_panel_id = Column(Text)
    referral_panel_display = Column(Text)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    referral_test = relationship('ReferralTest')


class ReferralParticipantAttachment(Base):
    __tablename__ = 'referral_participant_attachment'
    __table_args__ = {'schema': 'public'}

    referral_participant_attachment_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_participant_uid = Column(ForeignKey('public.referral_participant.referral_participant_uid'), nullable=False)
    attachment_uid = Column(ForeignKey('public.attachment.attachment_uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    attachment = relationship('Attachment')
    referral_participant = relationship('ReferralParticipant')


class ReferralSample(Base):
    __tablename__ = 'referral_sample'
    __table_args__ = {'schema': 'public'}

    referral_sample_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    sample_uid = Column(ForeignKey('public.sample.sample_uid'), nullable=False)
    referral_uid = Column(ForeignKey('public.referral.referral_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    referral = relationship('Referral')
    sample = relationship('Sample')


class ReferralTestTargetRegion(Base):
    __tablename__ = 'referral_test_target_region'
    __table_args__ = {'schema': 'public'}

    referral_test_target_region_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_test_uid = Column(ForeignKey('public.referral_test.referral_test_uid', ondelete='CASCADE'), nullable=False)
    referral_test_target_region = Column(Text, nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    referral_test = relationship('ReferralTest')


class ReferralTestTargetVariant(Base):
    __tablename__ = 'referral_test_target_variant'
    __table_args__ = {'schema': 'public'}

    referral_test_target_variant_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    referral_test_uid = Column(ForeignKey('public.referral_test.referral_test_uid', ondelete='CASCADE'), nullable=False)
    referral_test_target_variant = Column(Text, nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    referral_test = relationship('ReferralTest')


class Consent(Base):
    __tablename__ = 'consent'
    __table_args__ = {'schema': 'public'}

    consent_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    patient_uid = Column(ForeignKey('public.patient.patient_uid'), nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.identifier_uid', ondelete='SET NULL'))
    status_cid = Column(ForeignKey('public.concept.concept_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    identifier = relationship('Identifier')
    patient = relationship('Patient')
    concept = relationship('Concept')


class ConsentQuestionnaire(Base):
    __tablename__ = 'consent_questionnaire'
    __table_args__ = {'schema': 'public'}

    consent_questionnaire_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    identifier_uid = Column(ForeignKey('public.identifier.identifier_uid'), nullable=False)
    version = Column(Text)
    name = Column(Text)
    title = Column(Text)
    status_cid = Column(ForeignKey('public.concept.concept_uid'), nullable=False)
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

    consent_document_reference_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(ForeignKey('public.consent.consent_uid', ondelete='SET NULL'))
    identifier_uid = Column(ForeignKey('public.identifier.identifier_uid', ondelete='SET NULL'))
    status_cid = Column(ForeignKey('public.concept.concept_uid'), nullable=False)
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

    consent_note_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(ForeignKey('public.consent.consent_uid'), nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.identifier_uid'), nullable=False)
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

    consent_organisation_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(ForeignKey('public.consent.consent_uid'), nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.identifier_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent = relationship('Consent')
    identifier = relationship('Identifier')


class ConsentQuestionnaireResponse(Base):
    __tablename__ = 'consent_questionnaire_response'
    __table_args__ = {'schema': 'public'}

    consent_questionnaire_response_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(ForeignKey('public.consent.consent_uid', ondelete='SET NULL'))
    identifier_uid = Column(ForeignKey('public.identifier.identifier_uid', ondelete='SET NULL'))
    status_cid = Column(ForeignKey('public.concept.concept_uid'), nullable=False)
    consent_questionnaire_response_authored = Column(DateTime, nullable=False)
    source_identifier_uid = Column(ForeignKey('public.identifier.identifier_uid'), nullable=False)
    consent_questionnaire_uid = Column(ForeignKey('public.consent_questionnaire.consent_questionnaire_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent_questionnaire = relationship('ConsentQuestionnaire')
    consent = relationship('Consent')
    identifier = relationship('Identifier', primaryjoin='ConsentQuestionnaireResponse.identifier_uid == Identifier.identifier_uid')
    identifier1 = relationship('Identifier', primaryjoin='ConsentQuestionnaireResponse.source_identifier_uid == Identifier.identifier_uid')
    concept = relationship('Concept')


class ConsentWitnes(Base):
    __tablename__ = 'consent_witness'
    __table_args__ = {'schema': 'public'}

    consent_witness_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_uid = Column(ForeignKey('public.consent.consent_uid'), nullable=False)
    consent_witness_url = Column(Text, nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.identifier_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent = relationship('Consent')
    identifier = relationship('Identifier')


class ConsentingParty(Base):
    __tablename__ = 'consenting_party'
    __table_args__ = {'schema': 'public'}

    consenting_party_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    identifier_uid = Column(ForeignKey('public.identifier.identifier_uid'), nullable=False)
    relationship_cid = Column(ForeignKey('public.concept.concept_uid', ondelete='SET NULL'))
    consent_uid = Column(ForeignKey('public.consent.consent_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent = relationship('Consent')
    identifier = relationship('Identifier')
    concept = relationship('Concept')


class CqItem(Base):
    __tablename__ = 'cq_item'
    __table_args__ = {'schema': 'public'}

    cq_item_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_questionnaire_uid = Column(ForeignKey('public.consent_questionnaire.consent_questionnaire_uid'), nullable=False)
    cq_item_link_id = Column(Text, nullable=False)
    cq_item_prefix = Column(Text)
    cq_item_text = Column(Text)
    cq_item_required = Column(Boolean)
    cq_item_read_only = Column(Boolean)
    cq_item_max_length = Column(Integer)
    cq_parent_item_uid = Column(ForeignKey('public.cq_item.cq_item_uid', ondelete='SET NULL'))
    cq_item_initial_bool = Column(Boolean)
    cq_item_initial_integer = Column(Integer)
    cq_item_initial_string = Column(Text)
    cq_item_initial_decimal = Column(Numeric)
    cq_item_initial_date = Column(Date)
    cq_item_initial_datetime = Column(DateTime)
    cq_item_initial_time = Column(Time)
    initial_attachment_uid = Column(ForeignKey('public.attachment.attachment_uid', ondelete='SET NULL'))
    cq_item_type_cid = Column(ForeignKey('public.concept.concept_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent_questionnaire = relationship('ConsentQuestionnaire')
    concept = relationship('Concept')
    parent = relationship('CqItem', remote_side=[cq_item_uid])
    attachment = relationship('Attachment')


class OrganisationConsent(Base):
    __tablename__ = 'organisation_consent'
    __table_args__ = {'schema': 'public'}

    organisation_consent_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    organisation_uid = Column(UUID, nullable=False)
    consent_uid = Column(ForeignKey('public.consent.consent_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent = relationship('Consent')


class CdrAuthor(Base):
    __tablename__ = 'cdr_author'
    __table_args__ = {'schema': 'public'}

    cdr_author_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_document_reference_uid = Column(ForeignKey('public.consent_document_reference.consent_document_reference_uid'), nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.identifier_uid'), nullable=False)
    cdr_author_type_cid = Column(ForeignKey('public.concept.concept_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept')
    consent_document_reference = relationship('ConsentDocumentReference')
    identifier = relationship('Identifier')


class CdrContent(Base):
    __tablename__ = 'cdr_content'
    __table_args__ = {'schema': 'public'}

    cdr_content_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_document_reference_uid = Column(ForeignKey('public.consent_document_reference.consent_document_reference_uid'), nullable=False)
    attachment_uid = Column(ForeignKey('public.attachment.attachment_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    attachment = relationship('Attachment')
    consent_document_reference = relationship('ConsentDocumentReference')


class CdrRelatesTo(Base):
    __tablename__ = 'cdr_relates_to'
    __table_args__ = {'schema': 'public'}

    cdr_relates_to_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    code_cid = Column(ForeignKey('public.concept.concept_uid'), nullable=False)
    consent_document_reference_uid = Column(ForeignKey('public.consent_document_reference.consent_document_reference_uid'), nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.identifier_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept')
    consent_document_reference = relationship('ConsentDocumentReference')
    identifier = relationship('Identifier')


class CqItemEnableWhen(Base):
    __tablename__ = 'cq_item_enable_when'
    __table_args__ = {'schema': 'public'}

    cq_item_enable_when_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    cq_item_uid = Column(ForeignKey('public.cq_item.cq_item_uid', ondelete='SET NULL'))
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

    cq_item_option_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    cq_item_uid = Column(ForeignKey('public.cq_item.cq_item_uid'), nullable=False)
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

    cqr_author_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_questionnaire_response_uid = Column(ForeignKey('public.consent_questionnaire_response.consent_questionnaire_response_uid'), nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.identifier_uid'), nullable=False)
    author_type_cid = Column(ForeignKey('public.concept.concept_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    concept = relationship('Concept')
    consent_questionnaire_response = relationship('ConsentQuestionnaireResponse')
    identifier = relationship('Identifier')


class CqrBasedOn(Base):
    __tablename__ = 'cqr_based_on'
    __table_args__ = {'schema': 'public'}

    cqr_based_on_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_questionnaire_response_uid = Column(ForeignKey('public.consent_questionnaire_response.consent_questionnaire_response_uid'), nullable=False)
    identifier_uid = Column(ForeignKey('public.identifier.identifier_uid'), nullable=False)
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent_questionnaire_response = relationship('ConsentQuestionnaireResponse')
    identifier = relationship('Identifier')


class CqrItem(Base):
    __tablename__ = 'cqr_item'
    __table_args__ = {'schema': 'public'}

    cqr_item_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    consent_questionnaire_response_uid = Column(ForeignKey('public.consent_questionnaire_response.consent_questionnaire_response_uid'), nullable=False)
    cqr_item_link_id = Column(Text, nullable=False)
    cqr_item_text = Column(Text, nullable=False)
    subject_identifier_uid = Column(ForeignKey('public.identifier.identifier_uid'), nullable=False)
    cqr_parent_item_uid = Column(ForeignKey('public.cqr_item.cqr_item_uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    consent_questionnaire_response = relationship('ConsentQuestionnaireResponse')
    parent = relationship('CqrItem', remote_side=[cqr_item_uid])
    identifier = relationship('Identifier')


class CqrAnswer(Base):
    __tablename__ = 'cqr_answer'
    __table_args__ = {'schema': 'public'}

    cqr_answer_uid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    cqr_item_uid = Column(ForeignKey('public.cqr_item.cqr_item_uid'), nullable=False)
    value_bool = Column(Boolean)
    value_decimal = Column(Numeric)
    value_integer = Column(Integer)
    value_date = Column(Date)
    value_datetime = Column(DateTime)
    value_time = Column(Time)
    value_string = Column(Text)
    value_attachment_uid = Column(ForeignKey('public.attachment.attachment_uid', ondelete='SET NULL'))
    last_updated_by = Column(String(255))
    last_updated_by_session = Column(String(255))
    last_updated = Column(DateTime, index=True)

    cqr_item = relationship('CqrItem')
    attachment = relationship('Attachment')
