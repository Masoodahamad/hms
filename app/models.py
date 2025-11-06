from .db import db
from datetime import date, datetime

class TimestampMixin(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Patient(TimestampMixin):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=True)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(16), nullable=True)
    phone = db.Column(db.String(32), nullable=True)
    address = db.Column(db.String(300), nullable=True)
    appointments = db.relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

class Doctor(TimestampMixin):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(200), unique=True, nullable=True)
    appointments = db.relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")

class Appointment(TimestampMixin):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    visit_time = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(32), default="scheduled", nullable=False)

    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("Doctor", back_populates="appointments")
