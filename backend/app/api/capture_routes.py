from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json

from app.database.dependencies import get_db

from app.models.capture import Capture
from app.schemas.capture_schema import CaptureRequest
from app.services.planner_engine import generate_action_plan
from app.models.action_plan import ActionPlan
from app.services.analyser import analyze_capture


router = APIRouter()


@router.post("/capture")
def create_capture(
    request: CaptureRequest,
    db: Session = Depends(get_db)
):

    analysis = analyze_capture(request.text)

    new_capture = Capture(
        original_text=request.text,
        intent=analysis.get("intent", "Task"),
        category=analysis.get("intent", "Task"),
        status="Pending",
        priority=request.priority
        if request.priority
        else analysis.get(
            "priority",
            "Medium"
        ),
        deadline=request.deadline,
        source=request.source,
        entities=json.dumps(
        analysis.get("entities", {})
    ),
        tags=json.dumps(
            analysis.get("tags", [])
        )
    )

    db.add(new_capture)
    db.commit()
    db.refresh(new_capture)

    steps = generate_action_plan(
    new_capture.original_text
)

    for index, step in enumerate(steps, start=1):

        new_step = ActionPlan(
            capture_id=new_capture.id,
            step_number=index,
            step_title=step["title"],
            step_description=step["description"],
            status="Pending"
        )

        db.add(new_step)

    db.commit()
    return {
        "message": "Capture saved successfully",
        "capture_id": new_capture.id,
        "analysis": analysis
    }
    