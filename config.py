import os
from dotenv import load_dotenv


load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
IMEI_API_KEY = os.getenv("IMEI_API_KEY")
IMEI_API_URL = os.getenv("IMEI_API_URL")
DB_PATH = os.getenv("DB_PATH")
