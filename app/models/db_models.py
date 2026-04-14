from sqlalchemy import Column, Integer, String
from app.db.base import Base


class PriorAuth(Base):
    __tablename__ = "prior_auths"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String)
    insurance_provider = Column(String)
    procedure_code = Column(String)
    diagnosis_code = Column(String)