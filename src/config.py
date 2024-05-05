import os

from dotenv import load_dotenv


load_dotenv()

# TG bot token
TOKEN = os.getenv("TOKEN")


# db
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB = os.getenv("POSTGRES_DB")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
ECHO = False
