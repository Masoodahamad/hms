from flask import Blueprint, request, jsonify
from . import crud
from .exceptions import NotFoundError, BadRequestError
from .emailer import send_email
from .batch_calc import average_age
from .scraper import get_hospital_info, get_disease_facts

api_bp = Blueprint("api", __name__)

# ---------- Error handlers ----------
@api_bp.errorhandler(NotFoundError)
def handle_not_found(err):
    return jsonify({"error": str(err)}), 404

@api_bp.errorhandler(BadRequestError)
def handle_bad_request(err):
    return jsonify({"error": str(err)}), 400

# ---------- Patients ----------
@api_bp.post("/patients")
def create_patient():
    data = request.get_json(force=True)
    p = crud.create_patient(**data)
    return jsonify({"id": p.id, "name": p.name, "email": p.email, "dob": p.dob.isoformat(), "address": p.address}), 201

@api_bp.get("/patients")
def list_patients():
    out = []
    for p in crud.list_patients():
        out.append({"id": p.id, "name": p.name, "email": p.email, "dob": p.dob.isoformat(), "age": p.age})
    return jsonify(out)

@api_bp.get("/patients/<int:pid>")
def get_patient(pid):
    p = crud.get_patient(pid)
    return jsonify({"id": p.id, "name": p.name, "email": p.email, "dob": p.dob.isoformat(), "age": p.age})

@api_bp.put("/patients/<int:pid>")
def update_patient(pid):
    data = request.get_json(force=True)
    p = crud.update_patient(pid, **data)
    return jsonify({"ok": True, "id": p.id})

@api_bp.delete("/patients/<int:pid>")
def delete_patient(pid):
    crud.delete_patient(pid)
    return jsonify({"ok": True})

# ---------- Doctors ----------
@api_bp.post("/doctors")
def create_doctor():
    data = request.get_json(force=True)
    d = crud.create_doctor(**data)
    return jsonify({"id": d.id}), 201

@api_bp.get("/doctors")
def list_doctors():
    out = [{"id": d.id, "name": d.name, "specialty": d.specialty} for d in crud.list_doctors()]
    return jsonify(out)

# ---------- Appointments ----------
@api_bp.post("/appointments")
def create_appointment():
    data = request.get_json(force=True)
    a = crud.create_appointment(**data)
    # Send background email if patient has email (simulated)
    try:
        p = crud.get_patient(a.patient_id)
        if p.email:
            send_email(p.email, "Appointment Scheduled", f"Your appointment ID {a.id} is scheduled.", background=True)
    except Exception:
        pass
    return jsonify({"id": a.id}), 201

@api_bp.get("/appointments")
def list_appointments():
    out = []
    for a in crud.list_appointments():
        out.append({
            "id": a.id,
            "patient_id": a.patient_id,
            "doctor_id": a.doctor_id,
            "visit_time": a.visit_time.isoformat(),
            "status": a.status,
        })
    return jsonify(out)

# ---------- Batch calc ----------
@api_bp.get("/analytics/average-age")
def avg_age():
    size = int(request.args.get("batch_size", 100))
    return jsonify({"average_age": average_age(size)})

# ---------- Scraper utils ----------
@api_bp.get("/info/hospitals")
def hospitals_info():
    return jsonify(get_hospital_info())

@api_bp.get("/info/disease/<name>")
def disease_facts(name):
    return jsonify({"name": name, "fact": get_disease_facts(name)})
