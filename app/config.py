import os

class Config:
    # Basic config
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    # Database
    DB_PATH = os.getenv("DB_PATH", "hms.db")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email (stub)
    SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "25"))
    FROM_EMAIL = os.getenv("FROM_EMAIL", "masoodahamad05@gmail.com")

    # Batch
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
