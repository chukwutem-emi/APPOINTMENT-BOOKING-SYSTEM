from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Boolean
from sqlalchemy.sql import func
import enum


db = SQLAlchemy()
class User(db.Model):
    __tablename__ = "user"
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(100))
    password      = db.Column(db.String(200))
    email_address = db.Column(db.String(200), unique=True)
    public_id     = db.Column(db.String(200))
    phone_number  = db.Column(db.String(14), unique=True)
    admin         = db.Column(Boolean, default=False)
    google_token  = db.Column(db.String(1000), nullable=False)
    created_at    = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at    = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    def __repr__(self):
        return f"User(username='{self.username}', password='{self.password}', email_address='{self.email_address}', public_id='{self.public_id}', phone_number='{self.phone_number}', admin='{self.admin}'"


class AppointmentTypes(enum.Enum):
    CONSULTATION        = "Consultation(HealthcareAppointment)"
    COUNSELING          = "Counseling(HealthcareAppointment)"
    DENTAL              = "Dental(HealthcareAppointment)"
    PHYSIOTHERAPY       = "PhysiotherapySession(HealthcareAppointment)"
    VACCINATION         = "Vaccination(HealthcareAppointment)"
    REAL_ESTATE         = "RealEstateAgentAppointment(ProfessionalServices)"
    BUSINESS            = "BusinessConsultation(ProfessionalServices)"
    FINANCIAL_ADVISORY  = "FinancialAdvisory(ProfessionalServices)"
    TUTORING_ONE_ON_ONE = "OneOnOneSession(EducationAndTutoring)"
    ACADEMIC_ADVISING   = "AcademicAdvising(EducationAndTutoring)"
    CAREER_COUNSELING   = "CareerCounseling(EducationAndTutoring)"
    ELECTRONICS_REPAIR  = "ElectronicsRepair(phones, laptop)(TechnicalAndRepairServices)"
    HOME_SERVICES       = "HomeServices(plumbing, electrical)-(TechnicalAndRepairServices)"

class Appointment(db.Model):
    __tablename__ = "appointment"
    id                       = db.Column(db.Integer, primary_key=True)
    user_id                  = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    personnel_id             = db.Column(db.Integer, db.ForeignKey("personnel.id", ondelete="CASCADE"))
    first_name               = db.Column(db.String(50))
    last_name                = db.Column(db.String(50))
    gender                   = db.Column(db.String(6))
    user_phone_number        = db.Column(db.String(14))
    address                  = db.Column(db.String(300))
    email_address            = db.Column(db.String(200))
    next_of_kin              = db.Column(db.String(200))
    next_of_kin_phone_number = db.Column(db.String(14))
    next_of_kin_address      = db.Column(db.String(300))
    duration                 = db.Column(db.Integer)
    price                    = db.Column(db.Float)
    personnel_role           = db.Column(db.String(200))
    personnel_tel            = db.Column(db.String(14))
    organization_name        = db.Column(db.String(200))
    organization_address     = db.Column(db.String(300))
    phone_repair_price       = db.Column(db.String(300))
    laptop_repair_price      = db.Column(db.String(300))
    appointment_types        = db.Column(db.String(200), nullable=False)
    appointment_time         = db.Column(db.Time, nullable=False)
    appointment_date         = db.Column(db.Date, nullable=False)
    appointment_endTime      = db.Column(db.Time, nullable=False)
    appointment_description  = db.Column(db.String(300), nullable=True)
    user                     = db.relationship("User", backref=db.backref("appointment", lazy=True))
    personnel                = db.relationship("Personnel", backref=db.backref("appointment", lazy=True))
    created_at               = db.Column(DateTime(timezone=True), server_default=func.now())
    update_at                = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"Appointment(user_id='{self.user_id}', first_name='{self.first_name}', last_name='{self.last_name}', laptop_repair_price='{self.laptop_repair_price}', appointment_types='{self.appointment_types}', address='{self.address}', email_address='{self.email_address}', gender='{self.gender}', duration='{self.duration}', location='{self.location}', next_of_kin='{self.next_of_kin}', next_of_kin_address='{self.next_of_kin_address}', next_of_kin_phone_number='{self.next_of_kin_phone_number}', price='{self.price}', phone_repair_price='{self.phone_repair_price}', organization_name='{self.organization_name}', tel='{self.tel}', user_phone_number='{self.user_phone_number}', appointment_time='{self.appointment_time}', appointment_description='{self.appointment_description}', appointment_date='{self.appointment_date}', organization_address='{self.organization_address}')"


class Personnel(db.Model):
    __tablename__ ="personnel"
    id                   = db.Column(db.Integer, primary_key=True)
    name                 = db.Column(db.String(100), nullable=False)
    role                 = db.Column(db.String(200), nullable=False)
    specialization       = db.Column(db.String(200), nullable=False)
    organization         = db.Column(db.String(200), nullable=False)
    organization_address = db.Column(db.String(300), nullable=False)
    email                = db.Column(db.String(200), unique=True, nullable=False)
    phone_number         = db.Column(db.String(200), nullable=False)
    created_at           = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at           = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"Personnel(name='{self.name}', role='{self.role}', specialization='{self.specialization}', organization='{self.organization}', email='{self.email}', phone_number='{self.phone_number}', created_at='{self.created_at}', updated_at='{self.updated_at}', organization_address='{self.organization_address}')"