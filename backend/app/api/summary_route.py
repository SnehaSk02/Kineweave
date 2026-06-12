from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from datetime import datetime

# from app.models.capture import Capture
# from app.models.action_plan import ActionPlan
from app.services.summary import generate_daily_summary

router = APIRouter()

@router.get("/daily-summary")
def get_daily_summary(date: str = Query(None, description="Date in YYYY-MM-DD format"), 
db: Session = Depends(get_db)):
    target_date = None
    if date:
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail="Invalid date format. Use YYYY-MM-DD."
            )
    try:
        summary_data = generate_daily_summary(db, target_date)
        return summary_data

    except Exception as e:
        print(f"Error generating daily summary: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate daily summary."
        )

