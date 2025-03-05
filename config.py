from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

#загрузка токена
TOKEN=os.getenv("TOKEN")