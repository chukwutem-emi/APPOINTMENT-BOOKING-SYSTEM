from src.flaskFile import app
from dotenv import load_dotenv
import os
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Boolean
from sqlalchemy.sql import func
import enum




load_dotenv()

mysql = MySQL()
mysql.init_app(app)

base_uri=os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_DATABASE_URI"] = base_uri



db = SQLAlchemy(app=app)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100))
    password=db.Column(db.String(200))
    email_address=db.Column(db.String(200), unique=True)
    public_id=db.Column(db.String(200))
    phone_number=db.Column(db.String(14), unique=True)
    admin=db.Column(Boolean, default=False)
    created_at=db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at=db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    def __repr__(self):
        return f"User(username='{self.username}', password='{self.password}', email_address='{self.email_address}', public_id='{self.public_id}', phone_number='{self.phone_number}', admin='{self.admin}')"


class AppointmentTypes(enum.Enum):
    CONSULTATION = "Consultation(HealthcareAppointment)"
    COUNSELING = "Counseling(HealthcareAppointment)"
    DENTAL = "Dental(HealthcareAppointment)"
    PHYSIOTHERAPY = "PhysiotherapySession(HealthcareAppointment)"
    VACCINATION = "Vaccination(HealthcareAppointment)"
    REAL_ESTATE = "RealEstateAgentAppointment(ProfessionalServices)"
    BUSINESS = "BusinessConsultation(ProfessionalServices)"
    FINANCIAL_ADVISORY = "FinancialAdvisory(ProfessionalServices)"
    TUTORING_ONE_ON_ONE = "OneOnOneSession(EducationAndTutoring)"
    ACADEMIC_ADVISING = "AcademicAdvising(EducationAndTutoring)"
    CAREER_COUNSELING = "CareerCounseling(EducationAndTutoring)"
    ELECTRONICS_REPAIR = "ElectronicsRepair(phones, laptop)(TechnicalAndRepairServices)"
    HOME_SERVICES = "HomeServices(plumbing, electrical)-(TechnicalAndRepairServices)"

class Appointment(db.Model):
    __tablename__ = "appointment"
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    first_name=db.Column(db.String(50))
    last_name=db.Column(db.String(50))
    gender=db.Column(db.String(6))
    user_phone_number=db.Column(db.String(14))
    address=db.Column(db.String(300))
    email_address=db.Column(db.String(200))
    next_of_kin=db.Column(db.String(200))
    next_of_kin_phone_number=db.Column(db.String(14))
    next_of_kin_address=db.Column(db.String(300))
    duration=db.Column(db.Integer)
    price=db.Column(db.Float)
    doctor=db.Column(db.String(200))
    hospital=db.Column(db.String(200))
    location=db.Column(db.String(300))
    tel=db.Column(db.String(14))
    consultant_name=db.Column(db.String(200))
    organization_name=db.Column(db.String(200))
    organization_address=db.Column(db.String(300))
    tutor=db.Column(db.String(200))
    institution_name=db.Column(db.String(300))
    phone_repair_price=db.Column(db.String(300))
    laptop_repair_price=db.Column(db.String(300))
    appointment_types=db.Column(db.String(200), nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_endTime = db.Column(db.Time, nullable=False)
    appointment_description = db.Column(db.String(300), nullable=True)
    user=db.relationship("User", backref=db.backref("appointment", lazy=True))
    created_at=db.Column(DateTime(timezone=True), server_default=func.now())
    update_at=db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"Appointment(user_id='{self.user_id}', first_name='{self.first_name}', last_name='{self.last_name}', laptop_repair_price='{self.laptop_repair_price}', appointment_types='{self.appointment_types}', tutor='{self.tutor}', address='{self.address}', email_address='{self.email_address}', gender='{self.gender}', consultant_name='{self.consultant_name}', doctor='{self.doctor}', duration='{self.duration}', institution_name='{self.institution_name}', location='{self.location}', next_of_kin='{self.next_of_kin}', next_of_kin_address='{self.next_of_kin_address}', next_of_kin_phone_number='{self.next_of_kin_phone_number}', price='{self.price}', phone_repair_price='{self.phone_repair_price}', organization_name='{self.organization_name}', tel='{self.tel}', user_phone_number='{self.user_phone_number}', appointment_time='{self.appointment_time}', appointment_description='{self.appointment_description}', appointment_date='{self.appointment_date}', organization_address='{self.organization_address}')"


   