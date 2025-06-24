# ollama_interface.py

import requests
from config import OLLAMA_URL, MODEL_NAME

def query_ollama(prompt, model_name=None):
    """
    Sends a prompt to the local Ollama server and returns the model's response.
    
    You can override the model by passing model_name, otherwise uses default from config.
    """
    model_to_use = model_name or MODEL_NAME

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model_to_use,
                "prompt": prompt,
                "stream": False
            },
            timeout=660
        )

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip()
        else:
            return f"[Error] Ollama responded with status code {response.status_code}: {response.text}"

    except requests.exceptions.RequestException as e:
        return f"[Exception] Failed to reach Ollama server: {e}"
