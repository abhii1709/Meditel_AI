from datetime import datetime
from models.appointments import Appointment
from models.doctors import Doctor
from models.patients import Patient

class MeditelSystem:
    def __init__(self):
        self.doctors = []
        self.patients = []
        self.appointments = []
    
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
        appt = Appointment(doctor, patient, date_time)
        self.appointments.append(appt)
        return appt
    
    def list_appointments(self):
        for a in self.appointments:
            print(a.describe())
    
   

system=MeditelSystem()
appointment=Appointment()
d1 = Doctor("Priya Sharma", 45, "Cardiologist")
p1 = Patient("Ravi Kumar", 32 ,"Chest Pain")  

 
system.add_doctor(d1)

system.add_patient(p1)  
appt = system.create_appointment(d1, p1, datetime(2025, 11, 11, 14, 30))

system.list_appointments()
appointment.complete(d1,p1,datetime(2025, 11, 11, 14, 30)) 