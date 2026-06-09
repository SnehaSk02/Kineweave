from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.capture import Capture
from app.models.action_plan import ActionPlan
from app.services.planner_engine import generate_action_plan

router = APIRouter()


@router.post("/generate-plan/{capture_id}")
def generate_plan(capture_id: int, db: Session = Depends(get_db)):
    print("Received capture_id:", capture_id)

    capture = db.query(Capture).filter(
        Capture.id == capture_id
    ).first()

    print("Capture object:", capture)
    
    if not capture:
        raise HTTPException(
            status_code=404,
            detail="Capture not found"
        )
    
    # Prevent duplicate plans
    existing_plan = db.query(ActionPlan).filter(
        ActionPlan.capture_id == capture_id
    ).first()

    if existing_plan:
        return {
            "message": "Plan already exists for this capture",
            "capture_id": capture_id
        }
    
    # Generate roadmap
    steps = generate_action_plan(
    capture.original_text
)

   # Save roadmap

    for index, step in enumerate(steps, start=1):

        new_step = ActionPlan(
        capture_id=capture.id,
        step_number=index,
        step_title=step["title"],
        step_description=step["description"],
        status="Pending"
        )

        db.add(new_step)

    db.commit()

    return {
    "message": "Plan generated successfully",
    "capture_id": capture.id,
    "steps_count": len(steps),
    "steps": steps
}

@router.get("/plans/{capture_id}")
def get_plan(
    capture_id: int,
    db: Session = Depends(get_db)
):

    plans = db.query(ActionPlan).filter(
        ActionPlan.capture_id == capture_id
    ).all()

    if not plans:
        raise HTTPException(
            status_code=404,
            detail="No plan found"
        )

    return plans