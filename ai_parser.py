import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schemas import CleanLeadData

# load the envornment variables from your .env file:
load_dotenv()

# Initialize the Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def parse_unstructured_text(raw_text: str) -> CleanLeadData:
    """ Uses Gemini to parse messy text directly into a structured Pydantic object """
    
    prompt = (
        "You are an elite data extraction assistant. Extract details from messy "
        f"incoming business alerts into a clean structure.\n\nInput Text:\n{raw_text}"
    )
    
    # Request a structured JSON payload matching our Pydantic blueprint
    response = client.models.generate_content(
        model='gemini-2.5-flash',  # Fast, lightweight, and perfect for structured processing
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CleanLeadData,
        ),
    )
    
    # response.text is guaranteed to be a valid JSON string matching CleanLeadData
    return CleanLeadData.model_validate_json(response.text)