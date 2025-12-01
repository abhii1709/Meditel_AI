from .person import Person
from contextlib import contextmanager

class Doctor(Person):
    
    doctors_created = 0
    
    def __init__(self, name: str, age: int, specialty: str, contact: str = None):
        super().__init__(name, age,contact)         # initialize parent (Person)
        self._specialty =None
        self.specialty = specialty
        Doctor.doctors_created +=1
    
    
    @property
    def specialty(self)->str:
        return self._specialty
    
    @specialty.setter
    def specialty(self,value:str):
         if not value or not value.strip():
             raise ValueError("Specialty cannot be empty.")
         self._specialty = value.strip().title()
        
    
        
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
        """Check if a given specialty is valid."""
        valid_specialties = [
            "Cardiology", "Dermatology", "Pediatrics",
            "Orthopedics", "Neurology", "ENT", "General Medicine","Surgeon",
            "Gynocologist"
        ]
        return spec.title() in valid_specialties
    
    def __str__(self):
        """User-friendly representation (for print)."""
        return f"Dr. {self.name} ({self.specialty})"

    def __repr__(self):
        """Developer-friendly representation (for debugging)."""
        return f"Doctor(name='{self.name}', age={self.age}, specialty='{self.specialty}')"

        
        