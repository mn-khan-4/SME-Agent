import re
import os
from config import TEMPLATE_DIR, HR_TEMPLATES_DIR  # ✅ Import HR path

def load_template(template_name):
    """Load a template file by name from Admin or HR folders."""
    admin_path = os.path.join(TEMPLATE_DIR, template_name)
    hr_path = os.path.join(HR_TEMPLATES_DIR, template_name)

    if os.path.exists(admin_path):
        with open(admin_path, "r", encoding="utf-8") as f:
            return f.read()
    elif os.path.exists(hr_path):
        with open(hr_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise FileNotFoundError(f"Template '{template_name}' not found in Admin or HR templates.")

def extract_placeholders(template_text):
    """Extract placeholders like {client_name}, {date}, etc."""
    return re.findall(r"{(.*?)}", template_text)

def fill_placeholders(template_text, values):
    """Replace placeholders with provided values."""
    for key, val in values.items():
        template_text = template_text.replace(f"{{{key}}}", val)
    return template_text

def build_prompt(user_query, top_k_results, metadata):
    """
    Creates a prompt combining the user query, template,
    and retrieved document metadata.
    """
    # ✅ Support both admin and HR templates
    template_name = next(
        (m["filename"] for m in top_k_results
         if isinstance(m, dict) and m.get("source") in ["template", "hr_template"]),
        None
    )

    if not template_name:
        raise ValueError("No matching template found in top_k_results.")

    template_text = load_template(template_name)
    placeholders = extract_placeholders(template_text)

    default_values = {
        # Admin
        "client_name": "John Doe",
        "billing_date": "2025-06-17",
        "due_date": "2025-06-30",
        "invoice_number": "INV-1001",
        "items": "- Web Design | 1 | PKR 200,000 | PKR 200,000",
        "subtotal": "PKR 200,000",
        "tax_rate": "15",
        "tax": "PKR 30,000",
        "grand_total": "PKR 230,000",
        "account_name": "ABC Agency",
        "bank_name": "Meezan Bank",
        "account_number": "123456789",
        "iban_swift": "PK00MEZN000000123456789",
        "additional_notes": "Payment due by end of month.",
        "project_description": "AI-based CRM system",
        "contractor_name": "Jane Smith",
        "duration": "1 year",
        "jurisdiction": "Pakistan",
        "quote_date": "2025-06-17",
        "validity_date": "2025-07-01",
        "client_business_name": "TechStart",
        "service_type": "Web Development",
        "hourly_rate": "5000",
        "estimated_hours": "50",
        "total_cost": "PKR 250,000",
        "payment_terms": "50% upfront, 50% after completion",
        "payment_method": "Bank Transfer",
        "your_email": "admin@smerouter.com",
        "your_phone": "+92-300-1234567",
        "your_name": "Admin Agent",
        "your_company_name": "SME Router",

        # HR
        "employee_name": "Ali Raza",
        "position": "Software Engineer",
        "joining_date": "2025-07-01",
        "salary": "PKR 120,000",
        "department": "IT",
        "manager": "Zara Khan",
        "leave_reason": "Medical emergency",
        "leave_start_date": "2025-06-22",
        "leave_end_date": "2025-06-27",
        "leave_days": "5",
    }

    selected_values = {k: v for k, v in default_values.items() if k in placeholders}
    filled_text = fill_placeholders(template_text, selected_values)

    final_prompt = f"""You are an AI Admin & HR Assistant. Based on the user's request, generate a professional business document.

User Query:
{user_query}

Document Type: {template_name.replace("template.txt", "").replace("", " ").title()}
Context Info: {metadata}

Filled Document:
{filled_text}

Respond ONLY with the document above. Do not explain anything.
"""

    return final_prompt