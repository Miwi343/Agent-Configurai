import os
from dotenv import load_dotenv

load_dotenv()

AUTOGEN_MODEL_API_KEY = os.getenv("AUTOGEN_MODEL_API_KEY")
AUTOGEN_MODEL_NAME = os.getenv("AUTOGEN_MODEL_NAME")