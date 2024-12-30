
from pydantic import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from secrets.env
load_dotenv("config/secrets.env")

class Settings(BaseSettings):
    APP_NAME: str = "ArcTecFox"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    class Config:
        env_file = "config/secrets.env"

# Create settings instance based on environment
settings = Settings()

# Load environment-specific settings
if settings.ENVIRONMENT == "production":
    from .prod_settings import ProdSettings
    settings = ProdSettings()
elif settings.ENVIRONMENT == "development":
    from .dev_settings import DevSettings
    settings = DevSettings()
