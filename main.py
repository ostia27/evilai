import os

import google.generativeai as genai
import typing_extensions as typing
from google.generativeai.types import HarmBlockThreshold, HarmCategory
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
main_config = genai.GenerationConfig(
    max_output_tokens=1000,
)

person = genai.protos.Schema(
    type = genai.protos.Type.OBJECT,
    properties = {
        'name':  genai.protos.Schema(type=genai.protos.Type.STRING),
        'description':  genai.protos.Schema(type=genai.protos.Type.STRING),
        'start_place_name': genai.protos.Schema(type=genai.protos.Type.STRING),
        'end_place_name': genai.protos.Schema(type=genai.protos.Type.STRING)
    },
    required=['name', 'description', 'start_place_name', 'end_place_name']
)

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction="talk like a pirate")
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"},
    ]
)
response = chat.send_message("I have 2 dogs in my house.")
print(response.text)
response = chat.send_message("How many paws are in my house?")
print(response.text)