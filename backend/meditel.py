from datetime import datetime
from backend.models.person import Person
from backend.models.doctors import Doctor
from backend.models.patients import Patient
from backend.models.appointment import Appointment
from backend.service.scheduler import Scheduler
from ai.ollama_client import Ollama_triage_client

class MeditelSystem:
    def __init__(self,use_ai=True):
        self.doctors = []
        self.patients = []
        self.appointments = []
        
        ollama_client = None
        if use_ai:
            ollama_client = Ollama_triage_client(model="llama3")
        
        self.scheduler = Scheduler(self.doctors, self.appointments,ollama_client)
       

    def add_doctor(self, doctor):
        self.doctors.append(doctor)

    def add_patient(self, patient):
        self.patients.append(patient)

    def find_doctor(self, name):
        return next((d for d in self.doctors if d.name == name), None)

    def create_appointment(self, doctor, patient, date_time):
        if doctor not in self.doctors:
            raise ValueError(f"Doctor {doctor.name} not found.")
        if patient not in self.patients:
            raise ValueError(f"Patient {patient.name} not found.")
        
        return self.scheduler.schedule(doctor, patient, date_time)

       

    def list_appointments(self):
        for a in self.appointments:
            print(a.describe())
            
    def find_doctor_by_specialty(self,specialty):
        return next(
            (d for d in self.doctors if d.specialty.lower() == specialty.lower()),
            None
        )
        
    
     
    def create_appointment_by_symptom(self, patient, symptom_text, date_time):
        

        if patient not in self.patients:
            raise ValueError(f"Patient {patient.name} not found in system.")
        return self.scheduler.schedule_by_symptom(patient, symptom_text, date_time)



def main():
    system = MeditelSystem(use_ai=True)

    d1 = Doctor("Priya Sharma", 45, "Cardiologist")
    system.add_doctor(d1)

    p1 = Patient("Ravi Kumar", 32, "Farting")
    system.add_patient(p1)

    appt = system.create_appointment_by_symptom(
        p1,
        "rashes",
        datetime(2025, 11, 11, 14, 30),
    )

    print("\n---- Appointment Created ----")
    system.list_appointments()

    appt.complete()

    print("\n---- After Completion ----")
    system.list_appointments()


if __name__ == "__main__":
    main()
