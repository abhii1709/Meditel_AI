from ai.ollama_client import Ollama_triage_client

client = Ollama_triage_client(model="llama3.2")

result = client.predict_specialty("chest pain and shortness of breath")
print("Predicted Specialty:", result)
