import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Load sensitive information from environment variables
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI
genai.configure(api_key=API_KEY)


model_chat_image = genai.GenerativeModel("gemini-pro-vision")


def generate_text_response(
    img,
    question: str = """<Question> : Identify the disease or plant or fruit or vegetable present in it ,explain what it is in clear.If it's a disease then explain it and provide medicine on it.""",
):

    # Get response from the gemini ai
    response = model_chat_image.generate_content([question, img])
    answer = response.text
    
    return answer
