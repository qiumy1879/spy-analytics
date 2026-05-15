from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    app_name: str = "Spy Analytics API"
    app_version: str = "0.1.0"
    
    # 使用绝对路径的 SQLite 数据库
    base_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    database_url: str = f"sqlite:///{os.path.join(base_dir, '..', 'spy_analytics.db')}"
    redis_url: str = "redis://localhost:6379/0"
    
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
