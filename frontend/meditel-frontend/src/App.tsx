import { useState, useEffect } from "react";
import {
  Calendar,
  User,
  Users,
  Clock,
  AlertCircle,
  Plus,
  Search,
  Activity,
  RefreshCw,
} from "lucide-react";
import {
  Doctor,
  Patient,
  Appointment,
  DoctorCreate,
  PatientCreate,
  AppointmentCreate,
} from "./types";

type Tab = "appointments" | "doctors" | "patients" | "create";

const API_BASE = "http://localhost:8000";

export default function MeditelApp() {
  const [activeTab, setActiveTab] = useState<Tab>("appointments");
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [patients, setPatients] = useState<Patient[]>([]);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");

  // Form states
  const [newDoctor, setNewDoctor] = useState<DoctorCreate>({
    name: "",
    age: 0,
    specialty: "",
    contact: "",
  });

  const [newPatient, setNewPatient] = useState<PatientCreate>({
    name: "",
    age: 0,
    symptoms: "",
  });

  const [newAppointment, setNewAppointment] = useState<AppointmentCreate>({
    patient_name: "",
    symptoms: "",
    scheduled_time: "",
  });

  // Fetch all data from backend
  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      // Fetch doctors
      const doctorsResponse = await fetch(`${API_BASE}/doctors`);
      if (!doctorsResponse.ok) throw new Error("Failed to fetch doctors");
      const doctorsData = await doctorsResponse.json();
      setDoctors(doctorsData);

      // Fetch patients
      const patientsResponse = await fetch(`${API_BASE}/patients`);
      if (!patientsResponse.ok) throw new Error("Failed to fetch patients");
      const patientsData = await patientsResponse.json();
      setPatients(patientsData);

      // Fetch appointments
      const appointmentsResponse = await fetch(`${API_BASE}/appointments`);
      if (!appointmentsResponse.ok)
        throw new Error("Failed to fetch appointments");
      const appointmentsData = await appointmentsResponse.json();
      setAppointments(appointmentsData);

      setSuccess("Data loaded successfully");
      setTimeout(() => setSuccess(null), 3000);
    } catch (error) {
      console.error("Error fetching data:", error);
      setError(
        "Failed to connect to backend. Make sure the server is running at http://localhost:8000"
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Create Doctor
  const handleCreateDoctor = async () => {
    if (!newDoctor.name || !newDoctor.specialty || !newDoctor.contact) {
      setError("Please fill all required fields");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/doctors`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newDoctor),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to create doctor");
      }

      // Add doctor to local state
      const createdDoctor: Doctor = {
        id: doctors.length + 1, // Note: Backend returns without ID, so we generate locally
        ...data.doctor,
      };

      setDoctors([...doctors, createdDoctor]);
      setNewDoctor({ name: "", age: 0, specialty: "", contact: "" });
      setSuccess("Doctor created successfully!");
      setTimeout(() => setSuccess(null), 3000);
      setActiveTab("doctors");
    } catch (error) {
      console.error("Error creating doctor:", error);
      setError(
        error instanceof Error ? error.message : "Failed to create doctor"
      );
    } finally {
      setLoading(false);
    }
  };

  // Create Patient
  const handleCreatePatient = async () => {
    if (!newPatient.name || newPatient.age <= 0) {
      setError("Please fill all required fields");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/patients`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newPatient),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to create patient");
      }

      // Add patient to local state
      const createdPatient: Patient = {
        id: patients.length + 1, // Note: Backend returns without ID
        ...data.patient,
      };

      setPatients([...patients, createdPatient]);
      setNewPatient({ name: "", age: 0, symptoms: "" });
      setSuccess("Patient created successfully!");
      setTimeout(() => setSuccess(null), 3000);
      setActiveTab("patients");
    } catch (error) {
      console.error("Error creating patient:", error);
      setError(
        error instanceof Error ? error.message : "Failed to create patient"
      );
    } finally {
      setLoading(false);
    }
  };

  // Create Appointment
  const handleCreateAppointment = async () => {
    if (!newAppointment.patient_name || !newAppointment.scheduled_time) {
      setError("Please select a patient and schedule time");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/appointments/by-symptom`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newAppointment),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to create appointment");
      }

      // Add appointment to local state
      const createdAppointment: Appointment = {
        id: appointments.length + 1,
        ...data,
        symptoms: newAppointment.symptoms,
      };

      setAppointments([...appointments, createdAppointment]);
      setNewAppointment({ patient_name: "", symptoms: "", scheduled_time: "" });
      setSuccess("Appointment created successfully!");
      setTimeout(() => setSuccess(null), 3000);
      setActiveTab("appointments");
    } catch (error) {
      console.error("Error creating appointment:", error);
      setError(
        error instanceof Error ? error.message : "Failed to create appointment"
      );
    } finally {
      setLoading(false);
    }
  };

  // Sync system to database (for initial setup)
  const handleSyncToDB = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/sync-system-to-db`, {
        method: "POST",
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error("Failed to sync with database");
      }

      setSuccess(
        `Sync completed: ${data.synced.doctors} doctors, ${data.synced.patients} patients synced`
      );
      setTimeout(() => setSuccess(null), 3000);

      // Refresh data after sync
      fetchData();
    } catch (error) {
      console.error("Error syncing:", error);
      setError("Failed to sync with database");
    } finally {
      setLoading(false);
    }
  };

  // Filter appointments for search
  const filteredAppointments = appointments.filter(
    (a) =>
      a.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.doctor_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.symptoms?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Helper function for status colors
  const getStatusColor = (status: string) => {
    switch (status) {
      case "Scheduled":
        return "bg-green-100 text-green-700";
      case "Completed":
        return "bg-blue-100 text-blue-700";
      case "Pending":
        return "bg-yellow-100 text-yellow-700";
      case "Cancelled":
        return "bg-red-100 text-red-700";
      default:
        return "bg-gray-100 text-gray-700";
    }
  };

  // Format date for display
  const formatDateTime = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleString("en-US", {
        weekday: "short",
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch (error) {
      return dateString;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-2 rounded-xl">
                <Activity className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Meditel</h1>
                <p className="text-sm text-gray-500">
                  Healthcare Appointment System
                </p>
                <p className="text-xs text-green-600 font-medium">
                  ✓ Connected to FastAPI Backend
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-6">
              <div className="text-center">
                <p className="text-2xl font-bold text-gray-900">
                  {appointments.length}
                </p>
                <p className="text-xs text-gray-500">Appointments</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-gray-900">
                  {doctors.length}
                </p>
                <p className="text-xs text-gray-500">Doctors</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-gray-900">
                  {patients.length}
                </p>
                <p className="text-xs text-gray-500">Patients</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Messages Display */}
      {error && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2">
          <div className="bg-red-50 border-l-4 border-red-400 p-4">
            <div className="flex">
              <AlertCircle className="h-5 w-5 text-red-400 mr-3" />
              <p className="text-sm text-red-700">{error}</p>
              <button
                onClick={() => setError(null)}
                className="ml-auto text-red-700 hover:text-red-600"
              >
                ×
              </button>
            </div>
          </div>
        </div>
      )}

      {success && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2">
          <div className="bg-green-50 border-l-4 border-green-400 p-4">
            <div className="flex">
              <AlertCircle className="h-5 w-5 text-green-400 mr-3" />
              <p className="text-sm text-green-700">{success}</p>
              <button
                onClick={() => setSuccess(null)}
                className="ml-auto text-green-700 hover:text-green-600"
              >
                ×
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-1 overflow-x-auto">
            {[
              {
                id: "appointments" as Tab,
                icon: Calendar,
                label: "Appointments",
                count: appointments.length,
              },
              {
                id: "doctors" as Tab,
                icon: Users,
                label: "Doctors",
                count: doctors.length,
              },
              {
                id: "patients" as Tab,
                icon: User,
                label: "Patients",
                count: patients.length,
              },
              { id: "create" as Tab, icon: Plus, label: "Create New" },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-6 py-4 border-b-2 transition-colors whitespace-nowrap ${
                  activeTab === tab.id
                    ? "border-blue-500 text-blue-600 bg-blue-50"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 hover:bg-gray-50"
                }`}
              >
                <tab.icon className="w-5 h-5" />
                <span className="font-medium">{tab.label}</span>
                {tab.count !== undefined && (
                  <span
                    className={`px-2 py-0.5 text-xs rounded-full ${
                      activeTab === tab.id
                        ? "bg-blue-100 text-blue-600"
                        : "bg-gray-100 text-gray-600"
                    }`}
                  >
                    {tab.count}
                  </span>
                )}
              </button>
            ))}

            {/* Sync Button */}
            <button
              onClick={handleSyncToDB}
              className="flex items-center space-x-2 px-6 py-4 text-gray-500 hover:text-gray-700 hover:border-gray-300 hover:bg-gray-50 border-b-2 border-transparent"
              title="Sync in-memory data to database"
            >
              <RefreshCw className="w-5 h-5" />
              <span className="font-medium">Sync to DB</span>
            </button>

            {/* Refresh Button */}
            <button
              onClick={fetchData}
              className="flex items-center space-x-2 px-6 py-4 text-gray-500 hover:text-gray-700 hover:border-gray-300 hover:bg-gray-50 border-b-2 border-transparent"
              title="Refresh data"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              <span className="font-medium">Refresh</span>
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            <span className="ml-3 text-gray-600">Loading...</span>
          </div>
        ) : (
          <>
            {activeTab === "appointments" && (
              <div className="space-y-6">
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900">
                      Appointments
                    </h2>
                    <p className="text-gray-600">
                      Manage and view all scheduled appointments
                    </p>
                  </div>
                  <div className="flex space-x-2">
                    <div className="relative w-full sm:w-64">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <input
                        type="text"
                        placeholder="Search appointments..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                  </div>
                </div>

                {filteredAppointments.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredAppointments.map((appointment) => (
                      <div
                        key={appointment.id}
                        className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                      >
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex items-center space-x-2">
                            <div className="bg-blue-100 p-2 rounded-lg">
                              <Calendar className="w-5 h-5 text-blue-600" />
                            </div>
                            <div>
                              <p className="text-sm font-medium text-gray-900">
                                {appointment.patient_name}
                              </p>
                              <p className="text-xs text-gray-500">Patient</p>
                            </div>
                          </div>
                          <span
                            className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(
                              appointment.status
                            )}`}
                          >
                            {appointment.status}
                          </span>
                        </div>

                        <div className="space-y-3">
                          <div className="flex items-center space-x-2 text-sm text-gray-600">
                            <Users className="w-4 h-4" />
                            <span className="font-medium">
                              Dr. {appointment.doctor_name}
                            </span>
                          </div>
                          <div className="flex items-center space-x-2 text-sm text-gray-600">
                            <Clock className="w-4 h-4" />
                            <span>
                              {formatDateTime(appointment.scheduled_time)}
                            </span>
                          </div>
                          {appointment.symptoms && (
                            <div className="pt-2 border-t border-gray-100">
                              <div className="flex items-start space-x-2 text-sm">
                                <AlertCircle className="w-4 h-4 mt-0.5 text-gray-400" />
                                <div>
                                  <p className="font-medium text-gray-700">
                                    Symptoms:
                                  </p>
                                  <p className="text-gray-600 mt-1">
                                    {appointment.symptoms}
                                  </p>
                                </div>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-12 bg-white rounded-xl border border-gray-200">
                    <Calendar className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      No appointments found
                    </h3>
                    <p className="text-gray-500 mb-6">
                      {searchTerm
                        ? "Try a different search term"
                        : "Get started by creating a new appointment"}
                    </p>
                    <button
                      onClick={() => setActiveTab("create")}
                      className="inline-flex items-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                    >
                      <Plus className="w-4 h-4 mr-2" />
                      Create Appointment
                    </button>
                  </div>
                )}
              </div>
            )}

            {activeTab === "doctors" && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">Doctors</h2>
                  <p className="text-gray-600">
                    Our team of medical specialists
                  </p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  {doctors.map((doctor) => (
                    <div
                      key={doctor.id}
                      className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                    >
                      <div className="flex flex-col items-center text-center">
                        <div className="bg-gradient-to-br from-purple-500 to-blue-500 p-4 rounded-full mb-4">
                          <Users className="w-8 h-8 text-white" />
                        </div>
                        <h3 className="text-lg font-semibold text-gray-900">
                          {doctor.name}
                        </h3>
                        <p className="text-sm text-blue-600 font-medium mt-1">
                          {doctor.specialty}
                        </p>
                        <div className="mt-4 space-y-2 text-sm text-gray-600 w-full">
                          <div className="flex justify-between">
                            <span className="text-gray-500">Age:</span>
                            <span className="font-medium">{doctor.age}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-500">Contact:</span>
                            <span className="font-medium truncate ml-2">
                              {doctor.contact}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === "patients" && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">Patients</h2>
                  <p className="text-gray-600">
                    Patient records and medical information
                  </p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  {patients.map((patient) => (
                    <div
                      key={patient.id}
                      className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                    >
                      <div className="flex flex-col">
                        <div className="flex items-center space-x-4">
                          <div className="bg-gradient-to-br from-green-500 to-teal-500 p-3 rounded-full">
                            <User className="w-6 h-6 text-white" />
                          </div>
                          <div className="flex-1">
                            <h3 className="text-lg font-semibold text-gray-900">
                              {patient.name}
                            </h3>
                            <p className="text-sm text-gray-500">
                              Age: {patient.age}
                            </p>
                          </div>
                        </div>
                        {patient.symptoms && (
                          <div className="mt-4 pt-4 border-t border-gray-100">
                            <p className="text-xs font-medium text-gray-700 mb-2">
                              Symptoms:
                            </p>
                            <p className="text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
                              {patient.symptoms}
                            </p>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === "create" && (
              <div className="space-y-8">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">
                    Create New
                  </h2>
                  <p className="text-gray-600">
                    Add new doctors, patients, or appointments
                  </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Create Doctor */}
                  <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center space-x-2 mb-6">
                      <div className="bg-gradient-to-br from-purple-500 to-blue-500 p-2 rounded-lg">
                        <Users className="w-5 h-5 text-white" />
                      </div>
                      <h3 className="text-xl font-semibold text-gray-900">
                        New Doctor
                      </h3>
                    </div>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Full Name *
                        </label>
                        <input
                          type="text"
                          value={newDoctor.name}
                          onChange={(e) =>
                            setNewDoctor({ ...newDoctor, name: e.target.value })
                          }
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                          placeholder="Dr. John Smith"
                        />
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Age *
                          </label>
                          <input
                            type="number"
                            value={newDoctor.age || ""}
                            onChange={(e) =>
                              setNewDoctor({
                                ...newDoctor,
                                age: parseInt(e.target.value) || 0,
                              })
                            }
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            placeholder="35"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Specialty *
                          </label>
                          <input
                            type="text"
                            value={newDoctor.specialty}
                            onChange={(e) =>
                              setNewDoctor({
                                ...newDoctor,
                                specialty: e.target.value,
                              })
                            }
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            placeholder="Cardiology"
                          />
                        </div>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Contact *
                        </label>
                        <input
                          type="text"
                          value={newDoctor.contact}
                          onChange={(e) =>
                            setNewDoctor({
                              ...newDoctor,
                              contact: e.target.value,
                            })
                          }
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                          placeholder="email@meditel.com"
                        />
                      </div>
                      <button
                        onClick={handleCreateDoctor}
                        disabled={loading}
                        className="w-full bg-gradient-to-r from-purple-500 to-blue-500 text-white py-3 rounded-lg font-medium hover:from-purple-600 hover:to-blue-600 transition-colors disabled:opacity-50"
                      >
                        {loading ? "Creating..." : "Add New Doctor"}
                      </button>
                    </div>
                  </div>

                  {/* Create Patient */}
                  <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center space-x-2 mb-6">
                      <div className="bg-gradient-to-br from-green-500 to-teal-500 p-2 rounded-lg">
                        <User className="w-5 h-5 text-white" />
                      </div>
                      <h3 className="text-xl font-semibold text-gray-900">
                        New Patient
                      </h3>
                    </div>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Full Name *
                        </label>
                        <input
                          type="text"
                          value={newPatient.name}
                          onChange={(e) =>
                            setNewPatient({
                              ...newPatient,
                              name: e.target.value,
                            })
                          }
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                          placeholder="Alice Brown"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Age *
                        </label>
                        <input
                          type="number"
                          value={newPatient.age || ""}
                          onChange={(e) =>
                            setNewPatient({
                              ...newPatient,
                              age: parseInt(e.target.value) || 0,
                            })
                          }
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                          placeholder="30"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Symptoms
                        </label>
                        <textarea
                          value={newPatient.symptoms}
                          onChange={(e) =>
                            setNewPatient({
                              ...newPatient,
                              symptoms: e.target.value,
                            })
                          }
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                          rows={3}
                          placeholder="Describe symptoms, medical history..."
                        />
                      </div>
                      <button
                        onClick={handleCreatePatient}
                        disabled={loading}
                        className="w-full bg-gradient-to-r from-green-500 to-teal-500 text-white py-3 rounded-lg font-medium hover:from-green-600 hover:to-teal-600 transition-colors disabled:opacity-50"
                      >
                        {loading ? "Creating..." : "Add New Patient"}
                      </button>
                    </div>
                  </div>
                </div>

                {/* Create Appointment */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center space-x-2 mb-6">
                    <div className="bg-gradient-to-br from-blue-500 to-purple-500 p-2 rounded-lg">
                      <Calendar className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900">
                      New Appointment
                    </h3>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Select Patient *
                        </label>
                        <select
                          value={newAppointment.patient_name}
                          onChange={(e) =>
                            setNewAppointment({
                              ...newAppointment,
                              patient_name: e.target.value,
                            })
                          }
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="">Choose a patient...</option>
                          {patients.map((patient) => (
                            <option key={patient.id} value={patient.name}>
                              {patient.name} (Age: {patient.age})
                            </option>
                          ))}
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Date & Time *
                        </label>
                        <input
                          type="datetime-local"
                          value={newAppointment.scheduled_time}
                          onChange={(e) =>
                            setNewAppointment({
                              ...newAppointment,
                              scheduled_time: e.target.value,
                            })
                          }
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                    </div>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Symptoms Description
                        </label>
                        <textarea
                          value={newAppointment.symptoms}
                          onChange={(e) =>
                            setNewAppointment({
                              ...newAppointment,
                              symptoms: e.target.value,
                            })
                          }
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent h-32"
                          placeholder="Describe the symptoms in detail. The system will automatically assign a suitable doctor based on symptoms."
                        />
                      </div>
                      <button
                        onClick={handleCreateAppointment}
                        disabled={loading}
                        className="w-full bg-gradient-to-r from-blue-500 to-purple-500 text-white py-3 rounded-lg font-medium hover:from-blue-600 hover:to-purple-600 transition-colors disabled:opacity-50"
                      >
                        {loading ? "Creating..." : "Schedule Appointment"}
                      </button>
                    </div>
                  </div>
                  <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
                    <p className="text-sm text-blue-700">
                      <span className="font-medium">Note:</span> The system will
                      automatically assign the most suitable doctor based on the
                      symptoms provided. Make sure you have doctors added first.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-3 mb-4 md:mb-0">
              <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-2 rounded-lg">
                <Activity className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="font-medium text-gray-900">
                  Meditel Healthcare System
                </p>
                <p className="text-sm text-gray-500">
                  v1.0.0 • React + TypeScript + Tailwind CSS • FastAPI Backend
                </p>
              </div>
            </div>
            <div className="text-sm text-gray-500">
              <p>Backend: {API_BASE} • CORS enabled for localhost:3000</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
