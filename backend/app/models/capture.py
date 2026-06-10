from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func

from app.database.db import Base


class Capture(Base):

    __tablename__ = "captures"

    id = Column(Integer, primary_key=True, index=True)

    original_text = Column(Text, nullable=False)

    intent = Column(String(50))

    category = Column(String(50))

    status = Column(String(20), default="Pending")

    priority = Column(String(20), default="Medium")

    deadline = Column(String(100), nullable=True)

    source = Column(String(50), default="text")

    progress = Column(Integer, default=0)

    entities = Column(JSON)

    tags=Column(JSON)
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )