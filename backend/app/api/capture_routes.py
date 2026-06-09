from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json

from app.database.dependencies import get_db

from app.models.capture import Capture
from app.schemas.capture_schema import CaptureRequest

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
        priority=analysis.get("priority", "Medium"),
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

    return {
        "message": "Capture saved successfully",
        "capture_id": new_capture.id,
        "analysis": analysis
    }