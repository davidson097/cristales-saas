from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "cristales"
    app_version: str = "0.1.0"
    
    # Database
    postgres_user: str = "cristales"
    postgres_password: str = "passcristales"
    postgres_db: str = "cristales_db"
    database_url: str = "postgresql://cristales:passcristales@localhost:5432/cristales_db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # API
    api_prefix: str = "/api/v1"
    
    # CORS
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"
    
    @property
    def db_host(self) -> str:
        # Extract host from DATABASE_URL
        if "localhost" in self.database_url:
            return "localhost"
        return "localhost"  # fallback
    
    @property
    def db_port(self) -> int:
        return 5432  # Extract from DATABASE_URL if needed
    
    @property
    def db_user(self) -> str:
        return self.postgres_user
    
    @property
    def db_password(self) -> str:
        return self.postgres_password
    
    @property
    def db_name(self) -> str:
        return self.postgres_db
    
    @property
    def cors_origins_list(self) -> list:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Allow extra fields from env


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
