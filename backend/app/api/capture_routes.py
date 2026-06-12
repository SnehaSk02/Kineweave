from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json

from app.database.dependencies import get_db

from app.models.capture import Capture
from app.models.action_plan import ActionPlan
from app.schemas.capture_schema import CaptureRequest
from app.services.analyser import analyze_capture
from app.services.planner_engine import generate_action_plan
from app.services.vector_store import store_capture

router = APIRouter()


@router.post("/capture")
def create_capture(
    request: CaptureRequest,
    db: Session = Depends(get_db)
):

    analysis = analyze_capture(
        request.text
    )

    captures = analysis.get(
        "captures",
        []
    )

    saved_captures = []

    for item in captures:

        new_capture = Capture(
            original_text=item.get(
                "text",
                ""
            ),
            intent=item.get(
                "intent",
                "Task"
            ),
            category=item.get(
                "intent",
                "Task"
            ),
            status="Pending",
            priority=request.priority if request.priority else item.get("priority","Medium"),
            deadline=request.deadline if request.deadline else item.get("deadline",""),
            entities=json.dumps(
                item.get(
                    "entities",
                    {}
                )
            ),
            tags=json.dumps(
                item.get(
                    "tags",
                    []
                )
            ),
            source="text"
        )

        db.add(new_capture)
        db.commit()
        db.refresh(new_capture)

        # storing capture (vector index)
        store_capture(
            capture_id=new_capture.id,
            text=item["text"],
            intent=item["intent"],
            tags=item["tags"]
            )

        # Generate roadmap

        steps = generate_action_plan( 
            item["text"]          #text send to planner
        )

        for index, step in enumerate(steps,start=1):
            if not isinstance(step, dict):
                continue
            new_step = ActionPlan(
                capture_id=new_capture.id,
                step_number=index,
                step_title=step.get(
                    "title",
                    f"Step {index}"
                ),
                step_description=step.get(
                    "description",
                    ""
                ),
                status="Pending"
            )

            db.add(new_step)
        db.commit()


        saved_captures.append(
            {
                "capture_id": new_capture.id,
                "text": item["text"],
                "intent": item["intent"],
                "priority": item["priority"],
                "steps_created": len(steps),
                "deadline": new_capture.deadline,

            }
        )

    return {
        "message":
        f"{len(saved_captures)} captures created",
        "captures":
        saved_captures
    }