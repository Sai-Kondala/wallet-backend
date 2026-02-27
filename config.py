import os

class Config:
    SECRET_KEY = "dev-secret-key"

    # Database
    DB_NAME = "wallet.db"

    # Session expiry
    SESSION_DURATION = 3600  # 1 hour

    # Flask
    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = False