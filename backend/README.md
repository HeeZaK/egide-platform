# Egide Backend (FastAPI)

Clean Architecture scaffold for the HRM and social-engineering simulation platform.

## Directory Tree

```text
backend/
├─ app/
│  ├─ main.py
│  ├─ api/
│  │  └─ v1/
│  │     ├─ router.py
│  │     └─ endpoints/
│  │        ├─ health.py
│  │        └─ osint.py
│  ├─ core/
│  │  ├─ config.py
│  │  └─ security.py
│  ├─ db/
│  │  ├─ base.py
│  │  └─ session.py
│  ├─ engines/
│  │  └─ osint_engine.py
│  ├─ models/
│  ├─ repositories/
│  ├─ schemas/
│  │  └─ osint.py
│  ├─ services/
│  │  └─ osint_service.py
│  └─ use_cases/
│     └─ enrich_email_profile.py
├─ tests/
│  └─ unit/
│     └─ test_osint_engine.py
└─ requirements.txt
```

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## OSINT Endpoint

- `POST /api/v1/osint/lookup`
- Body:

```json
{
  "email": "alice.martin@example.com"
}
```
