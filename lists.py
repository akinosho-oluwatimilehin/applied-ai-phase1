from google import genai
from google.genai import types
from dotenv import load_dotenv
from waste_request import  WasteRequest

load_dotenv()

client = genai.Client()

parsed_requests = []
customer_message = [
   "My bin wasn't collected yesterday.",
    "I need a new waste bin.",
    "Help me ehhhhhh"
]

def parse_waste_request(customer_message):
   prompt = f"""You are a working as customer attendant in customer support, 
   extract relevant information from customer complaints message.

   Customer message: {customer_message}
   """
    "The lid of my bin is broken.",

   response = client.models.generate_content(
      model = "gemini-3.8-flash",
      contents = prompt,
      config = types.GenerateContentConfig(
         response_mime_type = "application/json",
         response_schema = WasteRequest
      )
   )

   validated_request = WasteRequest.model_validate_json(response.text)
   return validated_request

for message in customer_message:
   result = parse_waste_request(message)
   parsed_requests.append(result)

for request in parsed_requests:
   print(request.model_dump_json(indent = 4))
   print("-----------------------------------------")