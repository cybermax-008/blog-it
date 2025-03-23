import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Choosen model
MODEL = 'gemini-2.0-flash'
DEFAULT_CONFIG = {
    'temperature': 0.3,
    'top_p': 0.95, 
    'top_k': 40,
    'max_output_tokens': 8192,
}

# content generation configuration
CONTENT_CONFIG = {
    'temperature': 0.7, # Higher temperature for more variety
    'top_p': 0.95, 
    'top_k': 40,
    'max_output_tokens': 8192,
}

# Podcast analysis configuration
ANALYSIS_CONFIG = {
    'temperature': 0.1, # Lower temperature for more deterministic results
    'top_p': 0.95,
    'top_k': 40,
    'max_output_tokens': 8192,
}

# Validation configuration
VALIDATION_CONFIG = {
    'temperature': 0.1, # Lower temperature for more deterministic results
    'top_p': 0.95,
    'top_k': 40,
    'max_output_tokens': 8192,
}

def configure_api():

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please enter your Gemini API key in the sidebar of the app")
    genai.configure(api_key=api_key)

def get_model(model_type="default", system_instruction=None):
    
    configure_api()

    if model_type == "content":
        config = CONTENT_CONFIG
    elif model_type == "analysis":
        config = ANALYSIS_CONFIG
    elif model_type == "validation":
        config = VALIDATION_CONFIG
    else:
        config = DEFAULT_CONFIG

    if system_instruction:
        return genai.GenerativeModel(MODEL, generation_config=config, system_instruction=system_instruction)
    else:
        return genai.GenerativeModel(MODEL, generation_config=config)
    return model


