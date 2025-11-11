from .person import Person
from contextlib import contextmanager

class Doctor(Person):
    
    doctors_created = 0
    
    def __init__(self, name: str, age: int, speciality: str, contact: str = None):
        super().__init__(name, age,contact)         # initialize parent (Person)
        self._speciality =None
        self.speciality = speciality
        Doctor.doctors_created +=1
    
    
    @property
    def speciality(self)->str:
        return self.speciality
    
    @speciality.setter
    def speciality(self,value:str):
         if not value or not value.strip():
             raise ValueError("Speciality cannot be empty.")
         self.speciality = value.strip().title()
        
    
        
    def describe(self):
        return f"Dr.{self.name}, age {self.age}, is a {self.speciality} doctor."
    
    def diagnose(self, patient_name: str):
        """Perform a diagnosis (for simulation)."""
        print(f"Dr. {self.name} is diagnosing {patient_name}...")
        
        
    @classmethod
    def total_doctors(cls) -> int:
        """Return total number of Doctor objects created."""
        return cls.doctors_created
    
    @staticmethod
    def validate_speciality(spec: str) -> bool:
        """Check if a given speciality is valid."""
        valid_specialities = [
            "Cardiology", "Dermatology", "Pediatrics",
            "Orthopedics", "Neurology", "ENT", "General Medicine","Surgeon",
            "Gynocologist"
        ]
        return spec.title() in valid_specialities
    
    def __str__(self):
        """User-friendly representation (for print)."""
        return f"Dr. {self.name} ({self.speciality})"

    def __repr__(self):
        """Developer-friendly representation (for debugging)."""
        return f"Doctor(name='{self.name}', age={self.age}, speciality='{self.speciality}')"

        
        