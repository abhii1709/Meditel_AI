from .person import Person

class Patient(Person):
    def __init__(self, name, age, symptoms):
        super().__init__(name, age)
        self.symptoms = symptoms or []
        
    
    def add_symptom(self, symptom):
        self.symptoms.append(symptom.strip().capitalize())               
    
    
    def describe(self):
        symptoms = ', '.join(self.symptoms) if self.symptoms else "No symptoms"
        return f"Patient {self.name}, Age {self.age}, Symptoms: {symptoms}"
        
       