from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.db.base import Base


class PriorAuth(Base):
    __tablename__ = "prior_auths"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String)
    insurance_provider = Column(String)
    procedure_code = Column(String)
    diagnosis_code = Column(String)
    status = Column(String, default="pending")
    notes = Column(String, default="")
    prior_auth_required = Column(Boolean, default=False)
    rule_reason = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)