import google.generativeai as genai
from dotenv import load_dotenv
import os
import traceback

load_dotenv()

# Load sensitive information from environment variables
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI
genai.configure(api_key=API_KEY)

# set generation config
generation_config = {
    "temperature": 0.35,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 500,
}

model_chat = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
)

def generate_text_response(question):
  """Generates a text response using a chat model, handling potential errors.

  Args:
      question: The question to be answered by the chat model.

  Returns:
      The generated text response, or an informative error message if an exception occurs.
  """

  try:
    chat = model_chat.start_chat(history=[])
    response = chat.send_message(question).text
    return response
  except Exception as e:
    error_message = f"An error occurred while generating a response: {traceback.format_exc()}"
    print(error_message)  # Log or handle the error as needed
    return "An error occurred. Please try again later."

