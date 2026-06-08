from app.database.db import engine
from app.models.capture import Capture
from app.database.db import Base

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")