from pydantic import BaseModel
from datetime import datetime

class AppointmentWithSymptomsRequest(BaseModel):
   patient_name:str
   symptoms:str
   scheduled_time:datetime    
   
   
class AppointmentResponseModel(BaseModel):
    doctor_name:str
    patient_name:str
    scheduled_time:datetime
    status:str