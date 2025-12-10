class Appointment:
    STATUS_SCHEDULED = "Scheduled"
    STATUS_COMPLETED = "Completed"
    STATUS_CANCELLED = "Cancelled"
    def __init__(self, doctor, patient, date_time):
        self.doctor = doctor
        self.patient = patient
        self.date_time = date_time
        self.status = Appointment.STATUS_SCHEDULED 

    def complete(self):
        self.status = Appointment.STATUS_COMPLETED

    def cancel(self):
        self.status = Appointment.STATUS_CANCELLED
   
   
   
    def describe(self):
        status = " (COMPLETED)" if self.is_completed else ""
        return (
            f"Appointment with Dr. {self.doctor.name} "
            f"for {self.patient.name} "
            f"on {self.date_time}{status}"
        )
