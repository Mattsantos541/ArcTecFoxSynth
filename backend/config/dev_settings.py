from pydantic_settings import BaseSettings
from .settings import Settings

class DevSettings(Settings):
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test.db"