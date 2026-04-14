from fastapi import FastAPI, HTTPException
from app.models.request import PriorAuthRequest
from app.models.db_models import PriorAuth
from app.db.session import SessionLocal, engine
from app.db.base import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Insurance Prior Auth API running"}


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.post("/prior-auth")
def create_prior_auth(request: PriorAuthRequest):
    db = SessionLocal()

    new_request = PriorAuth(
        patient_name=request.patient_name,
        insurance_provider=request.insurance_provider,
        procedure_code=request.procedure_code,
        diagnosis_code=request.diagnosis_code
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    db.close()

    return {"message": "Saved to database", "id": new_request.id}


@app.get("/prior-auths")
def get_prior_auths():
    db = SessionLocal()
    records = db.query(PriorAuth).all()
    results = []

    for r in records:
        results.append({
            "id": r.id,
            "patient_name": r.patient_name,
            "insurance_provider": r.insurance_provider,
            "procedure_code": r.procedure_code,
            "diagnosis_code": r.diagnosis_code,
        })

    db.close()
    return results


@app.get("/prior-auths/{auth_id}")
def get_prior_auth(auth_id: int):
    db = SessionLocal()
    record = db.query(PriorAuth).filter(PriorAuth.id == auth_id).first()

    if not record:
        db.close()
        raise HTTPException(status_code=404, detail="Prior auth not found")
   result = {
        "id": record.id,
        "patient_name": record.patient_name,
        "insurance_provider": record.insurance_provider,
        "procedure_code": record.procedure_code,
        "diagnosis_code": record.diagnosis_code,
    }

    db.close()
    return result
