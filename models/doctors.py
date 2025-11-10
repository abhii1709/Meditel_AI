from .person import Person

class Doctor(Person):
    def __init__(self, name, age, speciality):
        super().__init__(name, age)         # initialize parent (Person)
        self.speciality = speciality
        
    def describe(self):
        print(f"{self.name}, age {self.age}, is a {self.speciality} doctor.")