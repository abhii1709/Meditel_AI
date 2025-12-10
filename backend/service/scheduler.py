from datetime import datetime
from backend.models.appointment import Appointment
from backend.models.doctors import Doctor
from backend.models.patients import Patient


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
                # ✅ NEW: agar comma hai to pehli specialty lo
                specialty = specialty.split(",")[0].strip()

                print(f"[OLLAMA AI] Predicted specialty: {specialty}")
                return specialty

        except Exception as e:
            print("[OLLAMA AI] Failed, fallback to rules:", e)

      text = symptom_text.lower()

      if "chest" in text or "heart" in text or "bp" in text:
           return "Cardiologist"

      if "skin" in text or "rash" in text or "itch" in text or "allergy" in text:
        return "Dermatologist"

      if "cough" in text or "cold" in text or "fever" in text:
        return "Physician"

      return "General Physician"


    # ---------- Doctor search ----------
    def find_doctor_by_specialty(self, specialty: str) -> Doctor | None:
        specialty = specialty.lower().strip()
        for d in self.doctors:
            if hasattr(d, "specialty") and d.specialty.lower().strip() == specialty:
                return d
        return None

    # ---------- Direct scheduling (doctor already decided) ----------
    def schedule(self, doctor: Doctor, patient: Patient, date_time: datetime) -> Appointment:
        if not self._is_doctor_available(doctor, date_time):
         raise ValueError(f"Doctor {doctor.name} is not available at this time.")
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

        if not self._is_doctor_available(doctor, date_time):
         raise ValueError(f"Doctor {doctor.name} is not available at this time.")

        appt = Appointment(doctor, patient, date_time)
        self.appointments.append(appt)
        return appt
    
    def _is_doctor_available(self, doctor: Doctor, date_time: datetime) -> bool:
        """Check karo ki given time pe doctor free hai ya nahi."""
        for appt in self.appointments:
            # same doctor + same time + still scheduled
            if (
                appt.doctor == doctor and
                appt.date_time == date_time and
                appt.status == Appointment.STATUS_SCHEDULED
            ):
                return False
        return True