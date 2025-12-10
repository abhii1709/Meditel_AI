from abc import ABC,abstractmethod
class Person(ABC):
    def __init__(self, name, age,contact:str=None):
         if not name.strip():
            raise ValueError("Name cannot be empty.")
         if age <= 0:
            raise ValueError("Age must be positive.")
         self.name = name
         self.age = age
         self.contact =contact

@abstractmethod
def describe(self)->str:
    """All subclasses must implement a describe method."""
    pass