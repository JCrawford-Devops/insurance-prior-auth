from fastapi import FastAPI, HTTPException, Query
from app.models.request import (
    PriorAuthRequest,
    PriorAuthStatusUpdate,
    PriorAuthNotesUpdate,
)
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
        diagnosis_code=request.diagnosis_code,
        status="pending",
        notes=request.notes,
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    result = {
        "message": "Saved to database",
        "id": new_request.id,
        "status": new_request.status,
        "notes": new_request.notes,
        "created_at": new_request.created_at,
        "updated_at": new_request.updated_at,
    }

    db.close()
    return result


@app.get("/prior-auths")
def get_prior_auths(
    status: str | None = Query(default=None),
    insurance_provider: str | None = Query(default=None),
    patient_name: str | None = Query(default=None),
    sort_by: str = Query(default="created_at"),
    sort_order: str = Query(default="desc"),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    db = SessionLocal()
    query = db.query(PriorAuth)

    if status:
        query = query.filter(PriorAuth.status == status)

    if insurance_provider:
        query = query.filter(PriorAuth.insurance_provider == insurance_provider)

    if patient_name:
        query = query.filter(PriorAuth.patient_name.ilike(f"%{patient_name}%"))

    allowed_sort_fields = {
        "created_at": PriorAuth.created_at,
        "updated_at": PriorAuth.updated_at,
        "patient_name": PriorAuth.patient_name,
        "insurance_provider": PriorAuth.insurance_provider,
        "status": PriorAuth.status,
    }

    if sort_by not in allowed_sort_fields:
        db.close()
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort_by. Allowed values: {', '.join(allowed_sort_fields.keys())}"
        )

    sort_column = allowed_sort_fields[sort_by]

    if sort_order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    elif sort_order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_order. Allowed values: asc, desc"
        )

    total_count = query.count()
    records = query.offset(offset).limit(limit).all()

    results = []
    for r in records:
        results.append({
            "id": r.id,
            "patient_name": r.patient_name,
            "insurance_provider": r.insurance_provider,
            "procedure_code": r.procedure_code,
            "diagnosis_code": r.diagnosis_code,
            "status": r.status,
            "notes": r.notes,
            "created_at": r.created_at,
            "updated_at": r.updated_at,
        })

    db.close()
    return {
        "total_count": total_count,
        "limit": limit,
        "offset": offset,
        "items": results,
    }


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
        "status": record.status,
        "notes": record.notes,
        "created_at": record.created_at,
        "updated_at": record.updated_at,
    }

    db.close()
    return result


@app.patch("/prior-auths/{auth_id}/status")
def update_prior_auth_status(auth_id: int, update: PriorAuthStatusUpdate):
    allowed_statuses = {"pending", "submitted", "approved", "denied"}

    if update.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Allowed values: {', '.join(sorted(allowed_statuses))}"
        )

    db = SessionLocal()
    record = db.query(PriorAuth).filter(PriorAuth.id == auth_id).first()

    if not record:
        db.close()
        raise HTTPException(status_code=404, detail="Prior auth not found")

    record.status = update.status
    db.commit()
    db.refresh(record)

    result = {
        "message": "Status updated",
        "id": record.id,
        "status": record.status,
        "updated_at": record.updated_at,
    }

    db.close()
    return result


@app.patch("/prior-auths/{auth_id}/notes")
def update_prior_auth_notes(auth_id: int, update: PriorAuthNotesUpdate):
    db = SessionLocal()
    record = db.query(PriorAuth).filter(PriorAuth.id == auth_id).first()

    if not record:
        db.close()
        raise HTTPException(status_code=404, detail="Prior auth not found")

    record.notes = update.notes
    db.commit()
    db.refresh(record)

    result = {
        "message": "Notes updated",
        "id": record.id,
        "notes": record.notes,
        "updated_at": record.updated_at,
    }

    db.close()
    return result