from datetime import datetime


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Doctor(Person):
    def __init__(self, name, age, speciality):
        super().__init__(name, age)         # initialize parent (Person)
        self.speciality = speciality
        
    def describe(self):
        print(f"{self.name}, age {self.age}, is a {self.speciality} doctor.")


class Patient(Person):
    def __init__(self, name, age, symptoms, bill_amount):
        super().__init__(name, age)
        self.symptoms = symptoms
        self.__bill_amount = bill_amount   # encapsulated variable (private)
        
    def describe(self):
        print(f"{self.name}, age {self.age}, is a patient with {self.symptoms}.")
    
    def add_bill_amount(self, amount):
        if amount < 0:
            raise ValueError("Invalid Amount")
        self.__bill_amount += amount      # shorthand for increment
    
    def show_bill(self):
        return f"Bill amount of {self.name} is ₹{self.__bill_amount}"


class Appointment:
    def __init__(self,doctor,patient,date_time):
        self.doctor = doctor
        self.patient =patient
        self.date_time = date_time
        self.status = "scheduled"
    
    def describe(self):
        return (f"Appointment: {self.patient.name} with Dr. {self.doctor.name} "
                f"on {self.date_time.strftime('%d-%b-%Y %H:%M')} [{self.status}]")
 

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