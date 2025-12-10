// Doctor Types
export interface Doctor {
  id: number;
  name: string;
  age: number;
  specialty: string;
  contact: string;
}

export interface DoctorCreate {
  name: string;
  age: number;
  specialty: string;
  contact: string;
}

export interface DoctorResponse {
  success: boolean;
  message: string;
  doctor: {
    name: string;
    age: number;
    specialty: string;
    contact: string;
  };
}

// Patient Types
export interface Patient {
  id: number;
  name: string;
  age: number;
  symptoms: string;
}

export interface PatientCreate {
  name: string;
  age: number;
  symptoms: string;
}

export interface PatientResponse {
  success: boolean;
  message: string;
  patient: {
    name: string;
    age: number;
    symptoms: string;
  };
}

// Appointment Types
export interface Appointment {
  id: number;
  doctor_name: string;
  patient_name: string;
  scheduled_time: string;
  status: string;
  symptoms?: string;
}

export interface AppointmentCreate {
  patient_name: string;
  symptoms: string;
  scheduled_time: string;
}

export interface AppointmentResponse {
  doctor_name: string;
  patient_name: string;
  scheduled_time: string;
  status: string;
}
