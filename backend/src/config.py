import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set it in the .env file or as an environment variable.")