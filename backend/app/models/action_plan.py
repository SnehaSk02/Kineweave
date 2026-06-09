from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.db import Base


class ActionPlan(Base):
    __tablename__ = "action_plans"

    id = Column(Integer, primary_key=True, index=True)

    capture_id = Column(Integer, ForeignKey("captures.id"))

    step_number = Column(Integer)

    step_title = Column(String(255))

    step_description = Column(String(500))

    status = Column(String(50), default="Pending")