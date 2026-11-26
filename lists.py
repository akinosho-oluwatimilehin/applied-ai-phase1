from waste_request import WasteRequest
from google import genai
from google.genai import types
from dotenv import load_dotenv
import time
import asyncio

load_dotenv()
client = genai.Client()
async_client = client.aio

customer_message = [
   "My bin has been misplaced, please attend to this soon.",
   "The bottom of my bin is ruined, there's a dent there!!!",
   "Help me ehhhhhh"
]

def validate_request(customer_message, request):
    if request.issue_type == "damaged_bin" and "misplaced" in customer_message.lower():
        return False

    return True


async def parse_waste_request(customer_message):
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
         response = await async_client.models.generate_content(
            model = "gemini-3.5-flash-lite",
            contents = prompt,
            config = types.GenerateContentConfig(
               response_mime_type="application/json",
               response_schema = WasteRequest
            )
         )
      
         validated_request = WasteRequest.model_validate_json(response.text)

         if validate_request(customer_message, validated_request):
            return validated_request

         else:
            print("Request failed semantic validation.")
            return None

      
      except Exception as e:
         print("Attempt", attempt + 1, "failed:", e)
         if attempt < 2:
            await asyncio.sleep(2)

   print("Failed after 3 attempt.")    
   return None

parsed_results = []
async def main(): 
   results = await asyncio.gather(
      *(parse_waste_request(message) for message in customer_message)
   )

   parsed_results = [result for result in results if result is not None]

   for result in parsed_results: 
      print(result.model_dump_json (indent = 4))

asyncio.run(main())


# from fastapi import FastAPI 
# from pydantic import BaseModel
# from gemini_waste_parser import parse_waste_request

# app = FastAPI()

# class Complaint(BaseModel):
#     customer_message: str

# @app.post("/complaints")
# async def submit_complaint(complaint : Complaint):
#     result = await parse_waste_request(complaint.customer_message)

#     if result is not None:
#         return result.model_dump()

#     else:
#         return {
#             "message" : "Unable to process complaint."
#         }

# {
#   "customer_message": "My bin hasn't been picked up even when it was scheduled to. The mess is almost attracting rodents, its disgusting. Why hasn't it been picked up???? Please do so soon. "
# }