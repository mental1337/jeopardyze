import os
# from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings:
    POSTGRES_DSN: str = os.getenv("POSTGRES_DSN")
    SQLITE_LOCAL_DSN: str = os.getenv("SQLITE_LOCAL_DSN")

class Secrets:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")

settings = Settings()
secrets = Secrets()


