from .person import Person

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
