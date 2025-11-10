from datetime import datetime
from models.appointments import Appointment
from models.doctors import Doctor
from models.patients import Patient

class MeditelSystem:
    def __init__(self):
        self.doctors = []
        self.patient = []
        self.appointments = []
    
    def add_doctor(self, doctor):
        self.doctors.append(doctor)

    def add_patient(self, patient):
        self.patient.append(patient)

    def create_appointment(self, doctor, patient, date_time):
        appointment = Appointment(doctor, patient, date_time)
        self.appointments.append(appointment)
        return appointment

    def list_appointments(self):
        for a in self.appointments:
            print(a.describe())
    
    def list_doctors(self):
        for d in self.doctors:
            print(d.describe())

system=MeditelSystem()
d1 = Doctor("Priya Sharma", 45, "Cardiologist")
p1 = Patient("Ravi Kumar", 32 ,"Chest Pain",500)   
 
system.add_doctor(d1)
system.list_doctors()
system.add_patient(p1)  
appt = system.create_appointment(d1, p1, datetime(2025, 11, 11, 14, 30))

system.list_appointments()