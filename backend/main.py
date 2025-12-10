from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from models.doctors import Doctor
from models.patients import Patient
from backend.meditel import MeditelSystem
from schemas.doctor_schemas import DoctorResponse, DoctorCreate
from schemas.appt_schema import AppointmentWithSymptomsRequest, AppointmentResponseModel
from schemas.patient_schema import PatientCreate, PatientResponse
from backend.database import engine, get_db, Base
from models.db_models import DoctorDB, PatientDB, AppointmentDB
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables
Base.metadata.create_all(bind=engine)


system = MeditelSystem(use_ai=True)

@app.post("/doctors", response_model=DoctorResponse)
def create_doctor(data: DoctorCreate, db: Session = Depends(get_db)):
    # Create DB entry
    db_doctor = DoctorDB(
        name=data.name,
        age=data.age,
        specialty=data.specialty,
        contact=data.contact
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    
    # Create Doctor object for system
    doctor = Doctor(
        name=data.name,
        age=data.age,
        specialty=data.specialty,
        contact=data.contact
    )
    system.add_doctor(doctor)
    
    return DoctorResponse(
        success=True,
        message="Doctor Created Successfully",
        doctor={
            "name": doctor.name,
            "age": doctor.age,
            "specialty": doctor.specialty,
            "contact": doctor.contact
        }
    )

@app.post("/patients", response_model=PatientResponse)
def add_patient(data: PatientCreate, db: Session = Depends(get_db)):
    # Create DB entry
    db_patient = PatientDB(
        name=data.name,
        age=data.age,
        symptoms=data.symptoms
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    # Create Patient object for system
    patient = Patient(
        data.name,
        data.age,
        data.symptoms,
    )
    system.add_patient(patient)
    
    return PatientResponse(
        success=True,
        message="Patient created successfully",
        patient={
            "name": patient.name,
            "age": patient.age,
            "symptoms": getattr(patient, "symptoms", None) 
                        or getattr(patient, "main_complaint", None),
        }
    )

@app.post("/appointments/by-symptom", response_model=AppointmentResponseModel)
def create_appointment_by_symptom(
    payload: AppointmentWithSymptomsRequest,
    db: Session = Depends(get_db)
):
    # Get patient from DB
    db_patient = db.query(PatientDB).filter(PatientDB.name == payload.patient_name).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Get patient from system
    patient = next(
        (p for p in system.patients if p.name == payload.patient_name),
        None
    )
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found in system")
    
    try:
        # Create appointment using system
        appt = system.create_appointment_by_symptom(
            patient,
            payload.symptoms,
            payload.scheduled_time,
        )
        
        # Get doctor from DB
        db_doctor = db.query(DoctorDB).filter(DoctorDB.name == appt.doctor.name).first()
        if not db_doctor:
            raise HTTPException(status_code=404, detail="Doctor not found in database")
        
        # Save appointment to DB
        db_appointment = AppointmentDB(
            doctor_id=db_doctor.id,
            patient_id=db_patient.id,
            scheduled_time=appt.date_time if isinstance(appt.date_time, datetime) else datetime.fromisoformat(appt.date_time),
            status=appt.status,
            symptoms=payload.symptoms
        )
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return AppointmentResponseModel(
        doctor_name=appt.doctor.name,
        patient_name=appt.patient.name,
        scheduled_time=appt.date_time,
        status=appt.status,
    )

@app.get("/doctors")
def get_doctors(db: Session = Depends(get_db)):
    doctors = db.query(DoctorDB).all()
    return [
        {
            "id": d.id,
            "name": d.name,
            "age": d.age,
            "specialty": d.specialty,
            "contact": d.contact
        }
        for d in doctors
    ]

@app.get("/patients")
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(PatientDB).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "symptoms": p.symptoms
        }
        for p in patients
    ]

@app.get("/appointments")
def get_appointments(db: Session = Depends(get_db)):
    appointments = db.query(AppointmentDB).all()
    return [
        {
            "id": a.id,
            "doctor_name": a.doctor.name,
            "patient_name": a.patient.name,
            "scheduled_time": a.scheduled_time,
            "status": a.status,
            "symptoms": a.symptoms
        }
        for a in appointments
    ]

# Optional: Endpoint to sync system data with DB
@app.post("/sync-system-to-db")
def sync_system_to_db(db: Session = Depends(get_db)):
    """Sync in-memory system data to database"""
    synced = {"doctors": 0, "patients": 0, "appointments": 0}
    
    # Sync doctors
    for doctor in system.doctors:
        existing = db.query(DoctorDB).filter(DoctorDB.name == doctor.name).first()
        if not existing:
            db_doctor = DoctorDB(
                name=doctor.name,
                age=doctor.age,
                specialty=doctor.specialty,
                contact=doctor.contact
            )
            db.add(db_doctor)
            synced["doctors"] += 1
    
    # Sync patients
    for patient in system.patients:
        existing = db.query(PatientDB).filter(PatientDB.name == patient.name).first()
        if not existing:
            db_patient = PatientDB(
                name=patient.name,
                age=patient.age,
                symptoms=getattr(patient, "symptoms", None) or getattr(patient, "main_complaint", None)
            )
            db.add(db_patient)
            synced["patients"] += 1
    
    db.commit()
    return {"message": "Sync completed", "synced": synced}