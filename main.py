# main.py

from rag.retriever import retrieve_relevant_docs
from prompts.prompt_builder import build_prompt
from ollama_interface import query_ollama
from hr_agent.handler import handle_hr_query       # 👤 HR Agent
from admin.handler import handle_admin_query       # 🧑‍💼 Admin Agent

# Basic keywords to route to agents
HR_KEYWORDS = ['appointment letter', 'offer letter', 'leave', 'salary', 'employee', 'joining']
ADMIN_KEYWORDS = ['memo', 'report', 'schedule', 'meeting', 'announcement', 'note', 'admin']

def is_hr_query(user_input):
    return any(keyword in user_input.lower() for keyword in HR_KEYWORDS)

def is_admin_query(user_input):
    return any(keyword in user_input.lower() for keyword in ADMIN_KEYWORDS)

def main():
    print("\n🤖 SME Admin Agent is ready!")
    user_query = input("Enter your query: ").strip()

    # 👉 HR Task Check
    if is_hr_query(user_query):
        print("\n📎 This seems like an HR task.")
        forward = input("➡  Should I forward it to the HR Agent? (yes/no): ").strip().lower()
        if forward.startswith("y"):
            response = handle_hr_query(user_query)
            print("\n📄 Generated Document (HR Agent):")
            print("=" * 60)
            print(response)
            print("=" * 60)
            return
        else:
            print("⚠  Not forwarding to HR Agent. Trying Admin...")

    # 👉 Admin Task Check
    if is_admin_query(user_query):
        print("\n🗂 This seems like an Admin task.")
        forward = input("➡  Should I forward it to the Admin Agent? (yes/no): ").strip().lower()
        if forward.startswith("y"):
            response = handle_admin_query(user_query)
            print("\n📄 Generated Document (Admin Agent):")
            print("=" * 60)
            print(response)
            print("=" * 60)
            return
        else:
            print("⚠  Not forwarding to Admin Agent. Trying default flow...")

    # 👉 Default fallback logic (RAG mode)
    print("\n🔍 Retrieving context...")
    top_matches = retrieve_relevant_docs(user_query, top_k=3)

    print("\n📚 Top matching documents/templates:")
    for match in top_matches:
        print(match)

    print("\n🧠 Building prompt...")
    full_prompt = build_prompt(user_query, top_matches, user_query)

    print("\n📨 Sending to Mistral (Ollama)...")
    response = query_ollama(full_prompt)

    print("\n📄 Generated Document (Default RAG Agent):")
    print("=" * 60)
    print(response)
    print("=" * 60)

if __name__ == "__main__":
    main()
