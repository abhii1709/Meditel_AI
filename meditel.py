from datetime import datetime
from models.person import Person
from models.doctors import Doctor
from models.patients import Patient
from models.appointment import Appointment


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
            
    def find_doctor_by_speciality(self,speciality):
        return next(
            (d for d in self.doctors if d.speciality.lower() == speciality.lower()),
            None
        )
        
    def _infer_speciality_from_symptoms(self, symptom_text: str) -> str:
         
         text = symptom_text.lower()

         if "chest" in text or "heart" in text or "bp" in text:
            return "Cardiologist"

         if "skin" in text or "rash" in text or "itch" in text or "allergy" in text:
            return "Dermatologist"

         if "cough" in text or "cold" in text or "fever" in text:
            return "Physician"

      
         return "General Physician"
     
    def create_appointment_by_symptom(self, patient, symptom_text, date_time):
        

        if patient not in self.patients:
            raise ValueError(f"Patient {patient.name} not found in system.")

        # 1) Symptoms -> specialty
        speciality = self._infer_speciality_from_symptoms(symptom_text)
        print(f"[DEBUG] Inferred specialty: {speciality}")

        # 2) Doctor dhundo
        doctor = self.find_doctor_by_speciality(speciality)
        if doctor is None:
            raise ValueError(f"No doctor found for speciality: {speciality}")

        # 3) Appointment create karo (pehle se existing method use kar rahe hain)
        appt = self.create_appointment(doctor, patient, date_time)
        return appt


def main():
    system = MeditelSystem()

    d1 = Doctor("Priya Sharma", 45, "Cardiologist")
    system.add_doctor(d1)

    p1 = Patient("Ravi Kumar", 32, "Chest Pain")
    system.add_patient(p1)

    appt = system.create_appointment_by_symptom(
        p1,
        "Chest Pain and breathlessness",
        datetime(2025, 11, 11, 14, 30),
    )

    print("\n---- Appointment Created ----")
    system.list_appointments()

    appt.complete()

    print("\n---- After Completion ----")
    system.list_appointments()


if __name__ == "__main__":
    main()
