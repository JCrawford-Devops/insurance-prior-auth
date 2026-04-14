from pydantic import BaseModel


class PriorAuthRequest(BaseModel):
    patient_name: str
    insurance_provider: str
    procedure_code: str
    diagnosis_code: str