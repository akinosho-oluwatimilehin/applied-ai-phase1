from dotenv import load_dotenv 
from google import genai

#load environment variables
load_dotenv()

#to create gemini client
client = genai.Client()

#to send a request to gemini
response = client.models.generate_content(
     model="gemini-3.6-flash",
     contents="Explain what an API is in simple terms."
)

#to display gemini response
print("Generated text: ")
print(response.text)

print("\n Response Type: ")
print(type(response))

print("\nUsage Metadata: ")
print(response.usage_metadata)