import json
import os
import re
from ollama_interface import query_ollama

# Path constants
TEMPLATE_DIR = "admin/templates/"
METADATA_PATH = "admin/metadata.json"
DATA_PATH = "admin/data.json"


def load_template(template_name):
    path = os.path.join(TEMPLATE_DIR, template_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Template '{template_name}' not found in {TEMPLATE_DIR}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_placeholders(template_text):
    """Find placeholders like {project_name}, {date}, etc."""
    return re.findall(r"{(.*?)}", template_text)


def fill_placeholders(template_text, values):
    """Replace placeholders in the template with actual values."""
    for key, val in values.items():
        template_text = template_text.replace(f"{{{key}}}", val)
    return template_text


def build_prompt(user_query, template_name, context_data):
    """
    Build a full prompt using template and data from data.json
    """
    template_text = load_template(template_name)
    placeholders = extract_placeholders(template_text)

    selected_values = {k: v for k, v in context_data.items() if k in placeholders}
    filled_text = fill_placeholders(template_text, selected_values)

    final_prompt = f"""
You are an Admin Assistant AI. Based on the user request below, generate a professional admin document.

User Request:
{user_query}

Template Used: {template_name}
Document Content:
{filled_text}

Respond ONLY with the filled document above, no explanation or extra text.
"""
    return final_prompt


def handle_admin_query(user_query):
    """
    Main function to handle admin query:
    - Match template based on intent
    - Fill placeholders
    - Generate prompt
    - Send to Ollama for document generation
    """
    # Load template metadata
    try:
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    except Exception as e:
        return f"[Error] Could not load metadata: {e}"

    # Determine appropriate template
    selected_template = "memo_template.txt"
    for entry in metadata:
        if entry.get("type", "").lower() in user_query.lower():
            selected_template = entry["filename"]
            break

    # Load contextual values from data.json
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            context_data = json.load(f)
    except Exception as e:
        return f"[Error] Could not load admin data: {e}"

    # Build prompt and query Ollama
    try:
        prompt = build_prompt(user_query, selected_template, context_data)
        response = query_ollama(prompt)
        return response
    except Exception as e:
        return f"[Error] Failed to generate document: {e}"
