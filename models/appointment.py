class Appointment:
    def __init__(self, doctor, patient, date_time):
        self.doctor = doctor
        self.patient = patient
        self.date_time = date_time
        self.is_completed = False

    def complete(self):
        self.is_completed = True

    def describe(self):
        status = " (COMPLETED)" if self.is_completed else ""
        return (
            f"Appointment with Dr. {self.doctor.name} "
            f"for {self.patient.name} "
            f"on {self.date_time}{status}"
        )
