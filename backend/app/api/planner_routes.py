from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.capture import Capture
from app.models.action_plan import ActionPlan
from app.services.planner_engine import generate_action_plan
from app.schemas.update_step_schema import StepStatusUpdate


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
    print("Generated steps:", steps)

   # Save roadmap

    for index, step in enumerate(steps, start=1):

        print("Step:", step)

        if not isinstance(step, dict):
            continue

        new_step = ActionPlan(
            capture_id=capture.id,
            step_number=index,
            step_title=step.get("title", f"Step {index}"),
            step_description=step.get("description", ""),
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

    return [
        {
            "id": plan.id,
            "capture_id": plan.capture_id,
            "step_number": plan.step_number,
            "step_title": plan.step_title,
            "step_description": plan.step_description,
            "status": plan.status
        }
        for plan in plans
]

@router.put("/plans/{plan_id}/status")
def update_plan_status(
    plan_id: int,
    status: str,
    db: Session = Depends(get_db)
):

    plan = db.query(ActionPlan).filter(
        ActionPlan.id == plan_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Plan step not found"
        )

    plan.status = status

    db.commit()
    db.refresh(plan)

    return {
        "message": "Status updated",
        "plan_id": plan.id,
        "status": plan.status
    }

@router.put("/plan-step/{step_id}")
def update_step_status(
    step_id: int,
    request: StepStatusUpdate,
    db: Session = Depends(get_db)
):

    step = db.query(ActionPlan).filter(
        ActionPlan.id == step_id
    ).first()

    if not step:
        raise HTTPException(
            status_code=404,
            detail="Step not found"
        )

    step.status = request.status

    db.commit()

    total_steps = db.query(ActionPlan).filter(
        ActionPlan.capture_id == step.capture_id
    ).count()

    completed_steps = db.query(ActionPlan).filter(
        ActionPlan.capture_id == step.capture_id,
        ActionPlan.status == "Completed"
    ).count()

    progress = int(
        (completed_steps / total_steps) * 100
    )

    capture = db.query(Capture).filter(
        Capture.id == step.capture_id
    ).first()

    capture.progress = progress

    if progress == 0:
        capture.status = "Pending"

    elif progress < 100:
        capture.status = "In Progress"

    else:
        capture.status = "Completed"

    db.commit()

    return {
        "message": "Step updated",
        "progress": progress,
        "goal_status": capture.status
    }

