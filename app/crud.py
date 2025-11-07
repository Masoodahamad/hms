"""
CRUD Operations (Data Access Layer)

This module provides all the functions to interact with the database
for the core models: Patient, Doctor, and Appointment.
It abstracts the database logic away from the API/route handlers.
"""

from datetime import datetime
from .db import db
from .models import Patient, Doctor, Appointment
from .exceptions import NotFoundError, BadRequestError

# ------------------ Patients ------------------

def create_patient(name, dob, email=None, gender=None, phone=None, address=None):
    """Creates a new patient record in the database.

    Args:
        name (str): The patient's full name.
        dob (str or date): The patient's date of birth.
                           If a string, must be in ISO format (YYYY-MM-DD).
        email (str, optional): The patient's email.
        gender (str, optional): The patient's gender.
        phone (str, optional): The patient's phone number.
        address (str, optional): The patient's address.

    Returns:
        Patient: The newly created Patient object.

    Raises:
        BadRequestError: If the 'dob' string is not in valid ISO format.
    """
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
    """Gets a single patient by their unique ID.

    Args:
        pid (int): The ID of the patient to retrieve.

    Returns:
        Patient: The found Patient object.

    Raises:
        NotFoundError: If no patient with the given ID exists.
    """
    p = db.session.get(Patient, pid)
    if not p:
        raise NotFoundError("Patient not found")
    return p

def list_patients():
    """Lists all patients in the database, ordered by ID descending.

    Returns:
        list[Patient]: A list of all Patient objects.
    """
    return Patient.query.order_by(Patient.id.desc()).all()

def update_patient(pid: int, **fields):
    """Updates an existing patient's information.

    Args:
        pid (int): The ID of the patient to update.
        **fields: Keyword arguments for the patient fields to update
                    (e.g., name="New Name", phone="12345").

    Returns:
        Patient: The updated Patient object.

    Raises:
        NotFoundError: If no patient with the given ID exists.
        BadRequestError: If 'dob' is provided as a badly formatted string.
    """
    p = get_patient(pid) # Raises NotFoundError if not found
    for k, v in fields.items():
        if k == "dob" and isinstance(v, str):
            try:
                v = datetime.fromisoformat(v).date()
            except ValueError:
                raise BadRequestError("DOB must be ISO date string YYYY-MM-DD")
        setattr(p, k, v)
    db.session.commit()
    return p

def delete_patient(pid: int):
    """Deletes a patient from the database.

    Args:
        pid (int): The ID of the patient to delete.

    Raises:
        NotFoundError: If no patient with the given ID exists.
    """
    p = get_patient(pid) # Raises NotFoundError if not found
    db.session.delete(p)
    db.session.commit()

# ------------------ Doctors ------------------

def create_doctor(name, specialty=None, email=None):
    """Creates a new doctor record in the database.

    Args:
        name (str): The doctor's full name.
        specialty (str, optional): The doctor's specialty.
        email (str, optional): The doctor's email.

    Returns:
        Doctor: The newly created Doctor object.
    """
    doc = Doctor(name=name, specialty=specialty, email=email)
    db.session.add(doc)
    db.session.commit()
    return doc

def get_doctor(did: int) -> Doctor:
    """Gets a single doctor by their unique ID.

    Args:
        did (int): The ID of the doctor to retrieve.

    Returns:
        Doctor: The found Doctor object.

    Raises:
        NotFoundError: If no doctor with the given ID exists.
    """
    d = db.session.get(Doctor, did)
    if not d:
        raise NotFoundError("Doctor not found")
    return d

def list_doctors():
    """Lists all doctors in the database, ordered by ID descending.

    Returns:
        list[Doctor]: A list of all Doctor objects.
    """
    return Doctor.query.order_by(Doctor.id.desc()).all()

def update_doctor(did: int, **fields):
    """Updates an existing doctor's information.

    Args:
        did (int): The ID of the doctor to update.
        **fields: Keyword arguments for the doctor fields to update
                    (e.g., specialty="Cardiology").

    Returns:
        Doctor: The updated Doctor object.

    Raises:
        NotFoundError: If no doctor with the given ID exists.
    """
    d = get_doctor(did) # Raises NotFoundError if not found
    for k, v in fields.items():
        setattr(d, k, v)
    db.session.commit()
    return d

def delete_doctor(did: int):
    """Deletes a doctor from the database.

    Args:
        did (int): The ID of the doctor to delete.

    Raises:
        NotFoundError: If no doctor with the given ID exists.
    """
    d = get_doctor(did) # Raises NotFoundError if not found
    db.session.delete(d)
    db.session.commit()

# ------------------ Appointments ------------------

def create_appointment(patient_id: int, doctor_id: int, visit_time, notes=None):
    """Creates a new appointment record.

    Args:
        patient_id (int): The ID of the patient.
        doctor_id (int): The ID of the doctor.
        visit_time (str or datetime): The time of the appointment.
                                     If str, must be in ISO format.
        notes (str, optional): Any notes for the appointment.

    Returns:
        Appointment: The new Appointment object.

    Raises:
        NotFoundError: If the patient_id or doctor_id does not exist.
        BadRequestError: If 'visit_time' is a badly formatted string.
    """
    if isinstance(visit_time, str):
        try:
            visit_time = datetime.fromisoformat(visit_time)
        except ValueError:
            raise BadRequestError("visit_time must be ISO datetime string")
    
    # ensure foreign keys exist
    get_patient(patient_id)
    get_doctor(doctor_id)
    
    appt = Appointment(patient_id=patient_id, doctor_id=doctor_id, visit_time=visit_time, notes=notes)
    db.session.add(appt)
    db.session.commit()
    return appt

def list_appointments():
    """Lists all appointments, ordered by visit time ascending.

    Returns:
        list[Appointment]: A list of all Appointment objects.
    """
    return Appointment.query.order_by(Appointment.visit_time.asc()).all()

def update_appointment(aid: int, **fields):
    """Updates an existing appointment.

    Args:
        aid (int): The ID of the appointment to update.
        **fields: Keyword arguments for the fields to update
                    (e.g., notes="Follow-up").

    Returns:
        Appointment: The updated Appointment object.

    Raises:
        NotFoundError: If no appointment with the given ID exists.
        BadRequestError: If 'visit_time' is a badly formatted string.
    """
    appt = db.session.get(Appointment, aid)
    if not appt:
        raise NotFoundError("Appointment not found")
    
    if "visit_time" in fields and isinstance(fields["visit_time"], str):
        try:
            fields["visit_time"] = datetime.fromisoformat(fields["visit_time"])
        except ValueError:
            raise BadRequestError("visit_time must be ISO datetime string")

    for k, v in fields.items():
        setattr(appt, k, v)
        
    db.session.commit()
    return appt

def delete_appointment(aid: int):
    """Deletes an appointment from the database.

    Args:
        aid (int): The ID of the appointment to delete.

    Raises:
        NotFoundError: If no appointment with the given ID exists.
    """
    appt = db.session.get(Appointment, aid)
    if not appt:
        raise NotFoundError("Appointment not found")
    
    db.session.delete(appt)
    db.session.commit()
