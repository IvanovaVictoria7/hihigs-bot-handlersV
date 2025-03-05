import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Загрузка токена
TOKEN = os.getenv("TOKEN")
