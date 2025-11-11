class Appointment:
     STATUS_SCHEDULED = "Scheduled"
     STATUS_COMPLETED = "Completed"
     STATUS_CANCELLED = "Cancelled"
     def __init__(self,doctor,patient,date_time):
        if not doctor or not patient:
            raise ValueError("Doctor and Patient are required.")
        self.doctor = doctor
        self.patient = patient
        self.date_time = date_time
        self.status = Appointment.STATUS_SCHEDULED
    
     def complete(self):
        self.status = Appointment.STATUS_COMPLETED

     def cancel(self):
        self.status = Appointment.STATUS_CANCELLED

     def describe(self):
        return (f"Appointment: {self.patient.name} with Dr. {self.doctor.name} "
                f"on {self.date_time.strftime('%d-%b-%Y %H:%M')} [{self.status}]")