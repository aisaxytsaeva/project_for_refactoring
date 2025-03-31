from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DB_ADDR: str = "db"
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    
    # JWT
    JWT_SECRET: str
    JWT_ACCESS_EXPIRE: int = 15
    JWT_REFRESH_EXPIRE: int = 43200
    JWT_REFRESH_LONG_EXPIRE: int = 2592000
    
    # MinIO
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_ENDPOINT: str = "minio"
    MINIO_PORT: int = 9000
    
    class Config:
        env_file = ".env"
        extra = "forbid"  # Оставляем запрет на дополнительные поля

settings = Settings()