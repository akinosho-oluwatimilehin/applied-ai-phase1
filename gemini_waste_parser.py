from waste_request import WasteRequest
from google import genai
from google.genai import types
from dotenv import load_dotenv
import time

load_dotenv()
client = genai.Client()

customer_message = [
   "My bin has been misplaced, please attend to this soon.",
   "The bottom of my bin is ruined, there's a dent there!!!",
   "Help me ehhhhhh"
]

def parse_waste_request(customer_message):
   prompt = f"""
      You are a customer attendant work with customer support for a waste management company.
      Your job is to extract relevant information from customer complaints.

      Do not manufacture information that the cutomer didn't provide.

      CLASSIFICATION RULES: 
      If a bin is physically damaged: damaged_bin
      If a bin is missing or misplaced: misplaced_bin
      If scheduled waste collection didn't happen at all: missed_pickup
      If waste collection is late but still expected: delayed_pickup
      Anything that doesn't fit in the classifications above: other

      IMPORTANT RULES:
      - Only extract information supported by the customer's message.
      - Do not invent missing information.
      - If information is unavaible, return null.


      customer_message = {customer_message}
   """
   for attempt in range(3):
      try:
         response = client.models.generate_content(
            model = "gemini-3.5-flash-lite",
            contents = prompt,
            config = types.GenerateContentConfig(
               response_mime_type="application/json",
               response_schema = WasteRequest
            )
         )
      
         validated_request = WasteRequest.model_validate_json(response.text)
         return validated_request

      
      except Exception as e:
         print("Attempt", attempt + 1, "failed:", e)
         if attempt < 2:
            time.sleep(2)

   print("Failed after 3 attempt.")    
   return None

parsed_results = []
for message in customer_message:
   result = parse_waste_request(message)

   if result is not None:
      parsed_results.append(result)

for result in parsed_results:
   print(result.model_dump_json(indent = 4))