from datetime import datetime
from models.appointment import Appointment
from models.doctors import Doctor
from models.patients import Patient


class Scheduler:
    def __init__(self, doctors: list, appointments: list,ollama_client=None):
    
        self.doctors = doctors
        self.appointments = appointments
        self.ollama_client = ollama_client

    # ---------- "AI" jaisa dimag: symptoms -> specialty ----------
    def _infer_specialty_from_symptoms(self, symptom_text: str) -> str:
        if self.ollama_client is not None:
         try:
            specialty = self.ollama_client.predict_specialty(symptom_text)

            if isinstance(specialty, str) and specialty.strip():
                print(f"[OLLAMA AI] Predicted specialty: {specialty}")
                return specialty.strip()

         except Exception as e:
            print("[OLLAMA AI] Failed, fallback to rules:", e)
        
        text = symptom_text.lower()

        if "chest" in text or "heart" in text or "bp" in text:
            return "Cardiologist"

        if "skin" in text or "rash" in text or "itch" in text or "allergy" in text:
            return "Dermatologist"

        if "cough" in text or "cold" in text or "fever" in text:
            return "Physician"

        # default fallback
        return "General Physician"

    # ---------- Doctor search ----------
    def find_doctor_by_specialty(self, specialty: str) -> Doctor | None:
        specialty = specialty.lower()
        for d in self.doctors:
            if hasattr(d, "specialty") and d.specialty.lower() == specialty:
                return d
        return None

    # ---------- Direct scheduling (doctor already decided) ----------
    def schedule(self, doctor: Doctor, patient: Patient, date_time: datetime) -> Appointment:
        appt = Appointment(doctor, patient, date_time)
        self.appointments.append(appt)
        return appt

    # ---------- Smart scheduling (sirf symptoms se) ----------
    def schedule_by_symptom(
        self,
        patient: Patient,
        symptom_text: str,
        date_time: datetime
    ) -> Appointment:
        # 1) symptoms -> specialty
        specialty = self._infer_specialty_from_symptoms(symptom_text)
        print(f"[DEBUG] Inferred specialty: {specialty}")

        # 2) specialty -> doctor
        doctor = self.find_doctor_by_specialty(specialty)
        if doctor is None:
            raise ValueError(f"No doctor found for specialty: {specialty}")

        # 3) appointment banao
        appt = Appointment(doctor, patient, date_time)
        self.appointments.append(appt)
        return appt