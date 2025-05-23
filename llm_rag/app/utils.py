import fitz
from dotenv import load_dotenv
import os
from openai import OpenAI

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = "\n".join(page.get_text() for page in doc)
    return text


# OpenAI API
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def get_completion(prompt, 
                   model="gpt-3.5-turbo",
                   temperature = 0.5):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model = model,
        messages = messages,
        temperature = temperature
    )
    return response.choices[0].message.content