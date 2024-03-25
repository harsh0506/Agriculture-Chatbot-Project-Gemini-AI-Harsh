from deep_translator import GoogleTranslator
from langdetect import detect

def convert_to_english(text: str, convert_to: str = "en") -> tuple:
    language = detect(text)

    translation = GoogleTranslator(source=language, target=convert_to).translate(text)

    return translation.strip(), language