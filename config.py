# config.py

# 🌐 URL of the local Ollama API server
OLLAMA_URL = "http://localhost:11434"

# 🤖 Name of the AI model to be used for generating documents
MODEL_NAME = "mistral"

# 📂 General RAG Template and Document Paths
TEMPLATE_DIR = "templates"
DOCS_PATH = "docs/sample_docs.json"
INDEX_PATH = "rag/index.faiss"

# 👥 HR Agent Paths
HR_TEMPLATES_DIR = "hr_agent/templates/"
HR_METADATA_PATH = "hr_agent/metadata.json"
HR_EMPLOYEE_DATA_PATH = "hr_agent/data.json"

# 🧑‍💼 Admin Agent Paths
ADMIN_TEMPLATES_DIR = "admin/templates/"
ADMIN_METADATA_PATH = "admin/metadata.json"
ADMIN_DOCS_PATH = "admin/data.json"
