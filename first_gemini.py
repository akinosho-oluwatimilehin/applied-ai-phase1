from dotenv import load_dotenv 
from google import genai

#load environment variables
load_dotenv()

#to create gemini client
client = genai.Client()

#to send a request to gemini
response = client.models.generate_content(
     model="gemini-3.8-flash",
     contents="Explain what an API is in simple terms."
)

#to display gemini response
print(response.text)