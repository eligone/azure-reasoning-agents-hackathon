import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_cloud_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Error: Missing GROQ_API_KEY inside your local environment setup.")
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key
    )
    return client

def get_model_target():
    return os.environ.get("MODEL_TARGET", "llama-3.3-70b-versatile")