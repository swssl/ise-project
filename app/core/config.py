"""Core configuration and settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """This settings class reads ists values from a .env file.
    """
    debug: bool = False
    
    secret_key: str = "prototype-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    gateway_timeout: int = 30
    max_retry_attempts: int = 3
    
    class Config:
        env_file = ".env"


settings = Settings()
