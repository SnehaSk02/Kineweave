from fastapi import FastAPI
from app.api.capture_routes import router as capture_router
from app.api.planner_routes import router as planner_router
from app.api.dashboard_routes import router as dashboard_router
app = FastAPI()
app.include_router(capture_router)
app.include_router(planner_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {"message": "Kineweave API Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

