from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "cristales"
    app_version: str = "0.1.0"
    
    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "cristales_admin"
    db_password: str = "cristales_pass"
    db_name: str = "cristales_db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # API
    api_prefix: str = "/api/v1"
    
    # CORS
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"
    
    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    @property
    def cors_origins_list(self) -> list:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
