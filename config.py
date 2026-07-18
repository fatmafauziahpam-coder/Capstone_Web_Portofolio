import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "capstone-secret-key")

    database_url = os.environ.get("DATABASE_URL")

    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = database_url or (
        "sqlite:///" + os.path.join(BASE_DIR, "database.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024