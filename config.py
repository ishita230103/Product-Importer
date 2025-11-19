import os

class Settings:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_URL = "sqlite:///./backend/test.db"
    REDIS_URL = "redis://localhost:6379/0"
    TMP_DIR = "./backend/tmp_uploads"
    PROGRESS_INTERVAL = 500
    BATCH_SIZE = 20000
    ALLOWED_ORIGINS = ["*"]

settings = Settings()
