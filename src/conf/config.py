class Config:
    DB_URL = "postgresql+asyncpg://appuser:not-a-secret-pass@localhost:5432/app"
    JWT_SECRET = "your_secret_key"
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_SECONDS = 3600


config = Config
