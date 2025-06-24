# hr_agent/prompt_builder.py

import os
import re
from config import TEMPLATE_DIR

HR_TEMPLATE_DIR = os.path.join(TEMPLATE_DIR, "../hr_agent/templates/")


def load_template(template_name):
    path = os.path.join(HR_TEMPLATE_DIR, template_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Template '{template_name}' not found in HR templates.")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_placeholders(template_text):
    return re.findall(r"{(.*?)}", template_text)


def fill_placeholders(template_text, values):
    for key, val in values.items():
        template_text = template_text.replace(f"{{{key}}}", val)
    return template_text


def build_hr_prompt(user_query, template_name):
    template_text = load_template(template_name)
    placeholders = extract_placeholders(template_text)

    default_values = {
        "employee_name": "Ali Khan",
        "designation": "Sales Executive",
        "start_date": "2025-07-01",
        "salary": "PKR 100,000",
        "department": "Sales",
        "manager_name": "Ms. Fatima",
        "leave_start_date": "2025-07-15",
        "leave_end_date": "2025-07-20",
        "leave_reason": "Family function",
        "joining_date": "2025-07-01",
        "company_name": "SME Router Pvt. Ltd.",
        "company_address": "123 Business Park, Lahore",
        "hr_email": "hr@smerouter.com"
    }

    selected_values = {k: v for k, v in default_values.items() if k in placeholders}
    filled_text = fill_placeholders(template_text, selected_values)

    final_prompt = f"""You are the HR Agent of SME Router. Generate a professional document based on the user request.

User Query:
{user_query}

Document Type: {template_name.replace("_template.txt", "")}
Filled Document:
{filled_text}

Only return the filled document. Do not include extra commentary.
"""
    return final_prompt
