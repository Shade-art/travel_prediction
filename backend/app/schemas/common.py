from pydantic import BaseModel
from typing import Optional

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    phase: str
    mock_data_loaded: bool
