from fastapi import FastAPI,HTTPException
from models.doctors import Doctor
from models.patients import Patient
from meditel import MeditelSystem
from schemas.doctor_schemas import DoctorResponse,DoctorCreate
from schemas.appt_schema import AppointmentWithSymptomsRequest,AppointmentResponseModel
from schemas.patient_schema import PatientCreate, PatientResponse

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
      
    system.add_doctor(doctor)
    
    return DoctorResponse(
        success=True,
        message = "Doctor Created Successfully",
        doctor=
        {"name":doctor.name,
        "age" : doctor.age,
        "specialty":doctor.specialty,
        "contact":doctor.contact}
    )
    
@app.post("/appointments/by-symptom",response_model=AppointmentResponseModel)
def create_appointment_by_symptom(payload:AppointmentWithSymptomsRequest):
    patient = next(
        (p for p in system.patients if p.name == payload.patient_name),
                   None
    )
    if patient is None:
        raise HTTPException(status_code=404,detail="patient not found")
    
    try :
        appt = system.create_appointment_by_symptom(
            patient,
            payload.symptoms,
            payload.scheduled_time,
        )
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    
    
    return AppointmentResponseModel(
         doctor_name=appt.doctor.name,
        patient_name=appt.patient.name,
        scheduled_time=appt.date_time,   # yahan tumhare Appointment class ka field naam use karo
        status=appt.status,
    )
    
    
@app.post("/patients", response_model=PatientResponse)
def add_patient(data: PatientCreate):

    # 1) Patient object banao
    patient = Patient(
        data.name,
        data.age,
        data.symptoms,  
    )

    # 2) System me add karo
    system.add_patient(patient)

    # 3) Response bana ke bhejo
    return PatientResponse(
        success=True,
        message="Patient created successfully",
        patient={
            "name": patient.name,
            "age": patient.age,
            # yahan bhi Patient class ke attribute se match karna:
            "symptoms": getattr(patient, "symptoms", None) 
                        or getattr(patient, "main_complaint", None),
        }
    )

@app.get("/doctors")
def get_doctors():
    result = []

    for d in system.doctors:
        result.append({
            "name": d.name,
            "age": d.age,
            "specialty": d.specialty,
            "contact": d.contact
        })

    return result

@app.get("/patients")
def get_patients():
    result = []

    for p in system.patients:
        result.append({
            "name": p.name,
            "age": p.age,
            "symptoms": getattr(p, "symptoms", None)
                        or getattr(p, "main_complaint", None)
        })

    return result

@app.get("/appointments")
def get_appointments():
    result = []

    for a in system.appointments:
        result.append({
            "doctor_name": a.doctor.name,
            "patient_name": a.patient.name,
            "scheduled_time": a.date_time,
            "status": a.status,
        })

    return result
