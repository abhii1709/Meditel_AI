import requests

class Ollama_triage_client:
    def __init__(self,model:str="llama3"):
        self.model =model
        self.url = "http://localhost:11434/api/generate"
        
    def predict_specialty(self, symptom_text: str) -> str:
        prompt = f"""
You are a medical triage assistant.
Given the patient's symptoms, return ONLY the medical specialty name.
No explanation.

Symptoms: {symptom_text}

Output format example:
Cardiologist,Deramtologist,Gyncologist 
"""

        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        response = requests.post(self.url, json=data, timeout=60)
        result = response.json()

        specialty = result["response"].strip()
        return specialty
        