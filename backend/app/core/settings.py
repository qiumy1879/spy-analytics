from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Spy Analytics API"
    app_version: str = "0.1.0"
    
    database_url: str = "postgresql://admin:password@localhost:5432/spy_analytics"
    redis_url: str = "redis://localhost:6379/0"
    
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()

