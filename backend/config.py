from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Configurazioni di autenticazione
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Credenziali admin (da spostare in un database in produzione)
    ADMIN_USERNAME: str = "aistruttore"
    ADMIN_PASSWORD: str = "FreeflyYourMind2024"
    
    # Configurazioni dell'applicazione
    APP_NAME: str = "Chunker API"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()