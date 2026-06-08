from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.capture_schema import CaptureRequest
from app.models.capture import Capture

from app.database.dependencies import get_db
from app.services.intent_engine import detect_intent
from app.services.entity_engine import extract_entities
from app.services.tag_engine import generate_tags

router = APIRouter()


@router.post("/capture")
def capture_thought(
    request: CaptureRequest,
    db: Session = Depends(get_db)
):
    
    # Detect intent using Groq
    try:
        intent = detect_intent(request.text)
    except Exception as e:
        print(f"Intent Detection Error: {e}")
        intent = "Task"

    # Detect entity
    try:
        entities = extract_entities(request.text)
    except Exception as e:
        print(f"Entity Detection Error: {e}")
        entities = {
        "person": [],
        "date": [],
        "time": [],
        "organization": [],
        "topic": []
        }

    # Generate Tags
    try:
        tags = generate_tags(request.text)

    except Exception as e:
        print(f"Tag Generation Error: {e}")
        tags = []

        # Create database record
    new_capture = Capture(
            original_text=request.text,
            intent=intent,
            status="Pending",
            priority="Medium",
            entities=entities,
            tags=tags)

    # Save to database
    db.add(new_capture)
    db.commit()
    db.refresh(new_capture)

    return {
        "message": "Thought captured successfully",
        "id": new_capture.id,
        "text": new_capture.original_text,
        "intent": new_capture.intent,
        "entities": new_capture.entities,
        "tags": new_capture.tags

    }