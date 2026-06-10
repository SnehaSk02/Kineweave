from pydantic import BaseModel
from typing import Optional


class CaptureRequest(BaseModel):
    text: str

    deadline: Optional[str] = None

    priority: Optional[str] = None

    source: Optional[str] = "text"