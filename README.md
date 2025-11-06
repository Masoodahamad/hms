# Hospital Management System (Backend Only)

A minimal, production-style Flask app (no frontend) for managing patients, doctors, and appointments.
It also includes a fake email service, a batch average-age analytics endpoint, and simple "scraper"
utilities that return sample data.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
# API docs (examples)
curl -X POST http://127.0.0.1:5000/api/patients -H 'Content-Type: application/json' \
  -d '{"name":"Alice","dob":"1990-01-01","email":"alice@example.com"}'
curl http://127.0.0.1:5000/api/patients
curl http://127.0.0.1:5000/api/analytics/average-age
```

## Project layout
```
hms/
├─ app/
│  ├─ __init__.py        # Flask app factory
│  ├─ config.py          # Settings (DB URL, SMTP, logging, batch size)
│  ├─ models.py          # SQLAlchemy models (Patient, Doctor, Appointment)
│  ├─ db.py              # DB initialization
│  ├─ crud.py            # CRUD operations
│  ├─ routes.py          # Flask routes / endpoints
│  ├─ emailer.py         # Email service (sync + background via ThreadPoolExecutor)
│  ├─ batch_calc.py      # Batch average-age calculation
│  ├─ scraper.py         # Placeholder scraper utilities
│  ├─ logger.py          # Logging setup
│  └─ exceptions.py      # Custom exceptions
├─ run.py                # Entry point
├─ client/
│  ├─ __init__.py
│  └─ cli.py             # Minimal CLI to call the API (requires `requests`)
├─ tests/
│  ├─ __init__.py
│  ├─ conftest.py
│  ├─ test_crud.py
│  └─ test_batch_calc.py
├─ requirements.txt
└─ README.md
```

## Running tests
```
pytest -q
```
