# app/config.py

import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")  # fallback for local dev
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
