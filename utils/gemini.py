import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate(prompt):
    try:
        return model.generate_content(prompt).text.strip()
    except:
        return "[Generation failed]"

def suggest_outline(topic, doc_type):
    prompt = f"Give me 8 professional {'section headings for a report' if doc_type=='docx' else 'slide titles'} on: {topic}. One per line."
    return [line.strip() for line in generate(prompt).split('\n') if line.strip()]

def refine_with_context(current_text, instruction, context=""):
    prompt = f"""Previous context: {context[-1000:] if context else 'None'}

Current text: {current_text}

Instruction: {instruction}

Return only improved text:"""
    return generate(prompt)