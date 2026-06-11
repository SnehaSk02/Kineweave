from fastapi import FastAPI
from app.api.capture_routes import router as capture_router
from app.api.planner_routes import router as planner_router
from app.api.dashboard_routes import router as dashboard_router
from app.database.db import Base, engine
from app. api.memory_chat_route import router as memory_chat_router

from app.models.capture import Capture
from app.models.action_plan import ActionPlan

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(capture_router)
app.include_router(planner_router)
app.include_router(dashboard_router)
app.include_router(memory_chat_router)

@app.get("/")
def root():
    return {"message": "Kineweave API Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

