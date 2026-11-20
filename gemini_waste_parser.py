from google import genai
from google.genai import types
from waste_request import WasteRequest
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

customer_message = """ My bin has a dent beneath is and the lid is broken.
All after the pickup and i need it fixed soon.
"""

prompt = f""" 
You are an assistant that extracts information from waste pickup requests.
Extract the relevant information from the customer's message.

Customer message:
{customer_message}
"""

response = client.models.generate_content(
     model="gemini-3.8-flash",
     contents = prompt,
     config = types.GenerateContentConfig(
        response_mime_type = "application/json",
        response_schema = WasteRequest
     )
)

validated_request = WasteRequest.model_validate_json(response.text)

print(validated_request.model_dump_json(indent = 4))
print(validated_request.issue_type)
print(validated_request.is_urgent)