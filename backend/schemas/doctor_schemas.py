from pydantic import BaseModel

class DoctorCreate(BaseModel):
    name : str
    age : int
    specialty:str
    contact:str



class DoctorResponse(BaseModel):
    success: bool
    message: str
    doctor: dict

    