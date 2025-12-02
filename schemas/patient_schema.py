from pydantic import BaseModel

class PatientCreate(BaseModel):
    name: str
    age: int
    symptoms: str   # ya main_complaint: str  (jo bhi tum Patient class me use karte ho)


class PatientResponse(BaseModel):
    success: bool
    message: str
    patient: dict