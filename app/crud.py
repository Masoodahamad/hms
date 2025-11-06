from datetime import datetime
from .db import db
from .models import Patient, Doctor, Appointment
from .exceptions import NotFoundError, BadRequestError

# ------------------ Patients ------------------
def create_patient(name, dob, email=None, gender=None, phone=None, address=None):
    try:
        if isinstance(dob, str):
            dob = datetime.fromisoformat(dob).date()
    except ValueError:
        raise BadRequestError("DOB must be ISO date string YYYY-MM-DD")
    patient = Patient(name=name, dob=dob, email=email, gender=gender, phone=phone, address=address)
    db.session.add(patient)
    db.session.commit()
    return patient

def get_patient(pid: int) -> Patient:
    p = db.session.get(Patient, pid)
    if not p:
        raise NotFoundError("Patient not found")
    return p

def list_patients():
    return Patient.query.order_by(Patient.id.desc()).all()

def update_patient(pid: int, **fields):
    p = get_patient(pid)
    for k, v in fields.items():
        if k == "dob" and isinstance(v, str):
            v = datetime.fromisoformat(v).date()
        setattr(p, k, v)
    db.session.commit()
    return p

def delete_patient(pid: int):
    p = get_patient(pid)
    db.session.delete(p)
    db.session.commit()

# ------------------ Doctors ------------------
def create_doctor(name, specialty=None, email=None):
    doc = Doctor(name=name, specialty=specialty, email=email)
    db.session.add(doc)
    db.session.commit()
    return doc

def get_doctor(did: int) -> Doctor:
    d = db.session.get(Doctor, did)
    if not d:
        raise NotFoundError("Doctor not found")
    return d

def list_doctors():
    return Doctor.query.order_by(Doctor.id.desc()).all()

def update_doctor(did: int, **fields):
    d = get_doctor(did)
    for k, v in fields.items():
        setattr(d, k, v)
    db.session.commit()
    return d

def delete_doctor(did: int):
    d = get_doctor(did)
    db.session.delete(d)
    db.session.commit()

# ------------------ Appointments ------------------
def create_appointment(patient_id: int, doctor_id: int, visit_time, notes=None):
    if isinstance(visit_time, str):
        visit_time = datetime.fromisoformat(visit_time)
    # ensure refs exist
    get_patient(patient_id); get_doctor(doctor_id)
    appt = Appointment(patient_id=patient_id, doctor_id=doctor_id, visit_time=visit_time, notes=notes)
    db.session.add(appt)
    db.session.commit()
    return appt

def list_appointments():
    return Appointment.query.order_by(Appointment.visit_time.asc()).all()

def update_appointment(aid: int, **fields):
    appt = db.session.get(Appointment, aid)
    if not appt:
        raise NotFoundError("Appointment not found")
    if "visit_time" in fields and isinstance(fields["visit_time"], str):
        fields["visit_time"] = datetime.fromisoformat(fields["visit_time"])
    for k, v in fields.items():
        setattr(appt, k, v)
    db.session.commit()
    return appt

def delete_appointment(aid: int):
    appt = db.session.get(Appointment, aid)
    if not appt:
        raise NotFoundError("Appointment not found")
    db.session.delete(appt)
    db.session.commit()
