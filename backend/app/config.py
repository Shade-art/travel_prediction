from pydantic import BaseModel
import os

class Settings(BaseModel):
    PROJECT_NAME: str = "NYC Taxi Transit Demand Analysis & Prediction System"
    API_V1_STR: str = "/api"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]

settings = Settings()
