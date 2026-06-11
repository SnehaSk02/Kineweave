from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import (
    get_db
)

from app.models.capture import Capture
from app.models.action_plan import ActionPlan

from app.services.memory_service import (
    find_related_memories
)

router = APIRouter()

@router.get("/memory-search")
def memory_search(
    query: str,
    db: Session = Depends(get_db)
):

    memories = find_related_memories(
        query=query,
        db=db
    )

    return {
        "results": [
            {
                "capture_id":
                item["capture"].id,

                "text":
                item["capture"].original_text,

                "intent":
                item["capture"].intent,

                "status":
                item["capture"].status,

                "distance":
                round(
                    item["distance"],
                    3
                )
            }
            for item in memories
        ]
    }

@router.get("/memory-details/{capture_id}")
def memory_details(
    capture_id: int,
    db: Session = Depends(get_db)
):

    capture = db.query(
        Capture
    ).filter(
        Capture.id == capture_id
    ).first()

    if not capture:

        return {
            "error":
            "Capture not found"
        }

    plans = db.query(
        ActionPlan
    ).filter(
        ActionPlan.capture_id
        == capture_id
    ).all()

    return {

        "capture_id":
        capture.id,

        "text":
        capture.original_text,

        "intent":
        capture.intent,

        "priority":
        capture.priority,

        "status":
        capture.status,

        "progress":
        capture.progress,

        "plans":
        [
            {
                "step_number":
                p.step_number,

                "title":
                p.step_title,

                "description":
                p.step_description,

                "status":
                p.status
            }
            for p in plans
        ]
    }