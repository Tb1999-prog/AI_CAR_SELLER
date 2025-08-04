from google import genai
from google.genai import types
from google.genai.types import (
    HarmCategory,
    HarmBlockThreshold,
    SafetySetting,
)


SAFETY_SETTINGS = [
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
]

GENERATION_CONFIG = (
    types.GenerateContentConfig(
        response_mime_type="application/json",
        temperature=0.5,
        top_p=0.8,
        max_output_tokens=20000,
        safety_settings=SAFETY_SETTINGS,
    ),
)

API_KEY = "AIzaSyBCAZLjUAL0X1MoQpCqprGjWgX_HjoIbLQ"

client = genai.Client(api_key=API_KEY)

data_path = "data/vehicle_inventory.json"
EMBED_PATH = "data/faiss_index.index"
META_PATH = "data/faiss_metadata.pkl"
DATABASE_URL = "sqlite:///./data/chat_history.db"
