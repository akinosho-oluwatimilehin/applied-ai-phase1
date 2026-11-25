from dotenv import load_dotenv
from google import genai
from waste_request import WasteRequest
from google.genai import types
import asyncio

load_dotenv()
client = genai.Client()
async_client = client.aio

customer_message = [
   "My bin is damaged, since the day of the pickup. I need it fixed soon!",
   "I haven't seen my bin for a while now",
   "The pickup truck didn't come the day it's supposed to",
   "Help me ehhhhhh"
]

def validate_request(customer_message, request):
   if request.issue_type == "damaged_bin" and "misplaced" in customer_message.lower():
      return False
   else: 
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
            contents = prompt,
            model = "gemini-3.5-flash-lite",
            config = types.GenerateContentConfig(
               response_mime_type = "application/json",
               response_schema = WasteRequest
            )
         )

         validated_request = WasteRequest.model_validate_json(response.text)
         if validate_request(customer_message, validated_request):
            return validated_request
         else: 
            print("Semantic Validation failed.")
            return None

      except Exception as e:
         print("Attempt", attempt + 1, "Failed:", e)
         if attempt < 2:
            await asyncio.sleep(2)

   else: 
      print("Failed after 3 requests.")
      return None

async def main():
   results = await asyncio.gather(
      *(parse_waste_request(message) for message in customer_message)
   )

   parsed_results = [result for result in results if result is not None]

   for result in parsed_results:
      print(result.model_dump_json(indent = 4))

asyncio.run(main())