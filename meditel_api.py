from fastapi import FastAPI
from models.doctors import Doctor
from meditel import MeditelSystem
from schemas.doctor_schemas import DoctorResponse,DoctorCreate


app = FastAPI()
system = MeditelSystem(use_ai=True)

@app.post("/doctors",response_model=DoctorResponse)
def create_doctor(data:DoctorCreate):
    
    doctor = Doctor(
        name =data.name,
        age = data.age,
        specialty=data.specialty,
        contact=data.contact
    )
      
    system.add_doctor(Doctor)
    
    return DoctorResponse(
        success=True,
        message = "Doctor Created Successfully",
        doctor=
        {"name":doctor.name,
        "age" : doctor.age,
        "specialty":doctor.specialty,
        "contact":doctor.contact}
    )