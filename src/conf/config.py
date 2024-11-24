class Config:
    DB_URL = "postgresql+asyncpg://appuser:not-a-secret-pass@localhost:5432/app"


config = Config
