import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

def generate_ai_recommendation_gemini(school_name, has_connectivity, connectivity_summary, tower_summary):
    """Uses Gemini AI to generate network infrastructure recommendations."""
    prompt = f"""
    You are an expert in network infrastructure.
    
    Analyze and suggest improvements for the following school:
    
    School Name: {school_name}
    
    Connectivity:
    - Has Connectivity: {has_connectivity}
    - Connectivity Summary: {connectivity_summary}
    - Tower Summary: {tower_summary}
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text  # Extract recommendation from Gemini's response
    except Exception as e:
        return f"Error generating recommendation: {e}"
