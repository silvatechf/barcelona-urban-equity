import os
import requests
import json
import logging
from dotenv import load_dotenv

load_dotenv()

class AIBriefer:
    """
    Strategic AI Engine specialized in Social Impact and Urban Equity.
    Analyzes Green Mobility Gentrification using LLM integration.
    Localized for Barcelona stakeholders (Spanish output).
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def generate_briefing(self, accuracy: float, correlation: float) -> str:
        if not self.api_key:
            return "Audit unavailable: Missing API KEY."

        prompt = (
            f"Actúa como un Auditor Social Urbano Senior para Barcelona Activa. "
            f"Analiza estas métricas: Precisión del Modelo (R2) = {accuracy:.2f}, "
            f"Correlación entre Movilidad Verde y Coste de Vivienda = {correlation:.4f}. "
            f"\n\nGenera un informe estratégico estructurado en exactamente 3 párrafos cortos: "
            f"Párrafo 1 (Diagnóstico): Analiza si la movilidad sostenible se está convirtiendo en un 'beneficio de élite' dada la correlación de {correlation:.4f}. "
            f"Párrafo 2 (Evidencia): Explica cómo el R2 de {accuracy:.2f} valida la fiabilidad de esta tendencia de gentrificación. "
            f"Párrafo 3 (Recomendación): Sugiere una política pública para el Ayuntamiento de Barcelona. "
            f"\n\nREGLAS CRÍTICAS: "
            f"1. RESPONDE TOTALMENTE EM ESPAÑOL. "
            f"2. No incluyas títulos, ni números, ni introducciones como 'Aquí está el informe'. "
            f"3. Empieza directamente con el análisis."
            f"\n\nLanguage: Spanish. Tone: Academic and Executive."
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "BCN Urban Equity Audit"
        }

        # Model Fallback Chain
        models_to_try = [
            "google/gemini-flash-1.5-8b", 
            "meta-llama/llama-3.1-8b-instruct:free",
            "mistralai/mistral-7b-instruct:free"
        ]

        for model in models_to_try:
            try:
                data = {
                    "model": model,
                    "messages": [
                        {
                            "role": "system", 
                            "content": "Eres un Auditor de Datos Sociales en Barcelona. Tu respuesta debe estar siempre en ESPAÑOL profesional."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1 
                }
                
                logging.info(f"Generating Spanish strategic briefing using: {model}")
                response = requests.post(self.url, headers=headers, data=json.dumps(data), timeout=12)
                
                if response.status_code == 200:
                    result = response.json()
                    if "choices" in result:
                        briefing = result["choices"][0]["message"]["content"].strip()
                        logging.info("✅ Spanish social impact briefing successfully generated.")
                        return briefing
                
                logging.warning(f"Model {model} returned status {response.status_code}")
                continue

            except Exception as e:
                logging.error(f"Execution failed for model {model}: {e}")
                continue

        return " Audit synthesis offline. Por favor, verifique las métricas en el panel."