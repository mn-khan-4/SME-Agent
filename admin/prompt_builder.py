import os
import json
import re

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
    """
    Extracts all {placeholders} from the template.
    """
    return re.findall(r"{(.*?)}", template_text)

def fill_placeholders(template_text, values):
    """
    Replaces placeholders with provided values.
    """
    for key, val in values.items():
        template_text = template_text.replace(f"{{{key}}}", val)
    return template_text

def get_template_for_intent(user_query):
    """
    Determines which template best fits the user's query.
    Falls back to memo_template.txt if no match found.
    """
    try:
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        for entry in metadata:
            if "intent" in entry and entry["intent"].lower() in user_query.lower():
                return entry.get("filename", "memo_template.txt")

    except Exception:
        pass

    return "memo_template.txt"

def load_context_data():
    """
    Loads context values from data.json for filling templates.
    """
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def build_admin_prompt(user_query):
    """
    Builds the final prompt for the admin agent based on:
    - user query
    - matching template
    - placeholder data
    """
    template_name = get_template_for_intent(user_query)
    template_text = load_template(template_name)
    placeholders = extract_placeholders(template_text)
    data = load_context_data()

    selected_values = {k: v for k, v in data.items() if k in placeholders}
    filled_text = fill_placeholders(template_text, selected_values)

    prompt = f"""
You are a smart Admin AI Agent. Generate the following document based on the user request.

User Query:
{user_query}

Document Template: {template_name}

Filled Document:
{filled_text}

Respond ONLY with the completed document, no extra commentary.
"""
    return prompt
