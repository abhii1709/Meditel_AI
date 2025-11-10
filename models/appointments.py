class Appointment:
    def __init__(self,doctor,patient,date_time):
        self.doctor = doctor
        self.patient =patient
        self.date_time = date_time
        self.status = "scheduled"
    
    def describe(self):
        return (f"Appointment: {self.patient.name} with Dr. {self.doctor.name} "
                f"on {self.date_time.strftime('%d-%b-%Y %H:%M')} [{self.status}]")