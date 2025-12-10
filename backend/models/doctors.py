from .person import Person
from contextlib import contextmanager

class Doctor(Person):
  
    
    def __init__(self, name: str, age: int, specialty: str, contact: str = None):
        super().__init__(name, age,contact)         # initialize parent (Person)
        self.specialty = specialty
        
    
    
   
    
        
    def describe(self):
        return f"Dr.{self.name}, age {self.age}, is a {self.specialty} doctor."
    
    def diagnose(self, patient_name: str):
        """Perform a diagnosis (for simulation)."""
        print(f"Dr. {self.name} is diagnosing {patient_name}...")
        
        
    @classmethod
    def total_doctors(cls) -> int:
        """Return total number of Doctor objects created."""
        return cls.doctors_created
    
    @staticmethod
    def validate_specialty(spec: str) -> bool:
        """Check if a given specialty is valid."""
        valid_specialties = [
    "Cardiologist",
    "Dermatologist",
    "Pediatrician",
    "Orthopedic Surgeon",
    "Neurologist",
    "ENT Specialist",
    "General Physician",
    "Surgeon",
    "Gynecologist"
]
        return spec.title() in valid_specialties
    


        
        