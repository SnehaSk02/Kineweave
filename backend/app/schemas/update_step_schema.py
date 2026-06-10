from pydantic import BaseModel

class StepStatusUpdate(BaseModel):
    status: str