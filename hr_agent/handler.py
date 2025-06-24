import os
from hr_agent.prompt_builder import build_hr_prompt
from ollama_interface import query_ollama


def handle_hr_query(user_query:str):
    """
    Route and handle HR-related tasks such as generating offer letters,
    appointment letters, or leave applications.
    """
    print("\n📂 HR Agent Activated")

    if "offer letter" in user_query.lower():
        template_name = "offer_letter_template.txt"
    elif "appointment letter" in user_query.lower():
        template_name = "appointment_letter_template.txt"
    elif "leave application" in user_query.lower():
        template_name = "leave_application_template.txt"
    else:
        return "❌ Sorry, I couldn't recognize the HR document type."

    prompt = build_hr_prompt(user_query, template_name)
    response = query_ollama(prompt)
    return response