from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.dependencies import get_db
from app.models.capture import Capture
from app.models.action_plan import ActionPlan

router = APIRouter()


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):

    total_captures = db.query(
        Capture
    ).count()

    total_plan_steps = db.query(
        ActionPlan
    ).count()

    completed_steps = db.query(
        ActionPlan
    ).filter(
        ActionPlan.status == "Completed"
    ).count()

    pending_steps = db.query(
        ActionPlan
    ).filter(
        ActionPlan.status == "Pending"
    ).count()

    completion_rate = 0

    if total_plan_steps > 0:

        completion_rate = round(
            (completed_steps / total_plan_steps) * 100,
            2
        )

    # Recent Captures

    recent_captures = db.query(
        Capture
    ).order_by(
        Capture.id.desc()
    ).limit(5).all()

    # Intent Analytics

    intent_stats = (
        db.query(
            Capture.intent,
            func.count(Capture.id)
        )
        .group_by(Capture.intent)
        .all()
    )

    # Priority Analytics

    priority_stats = (
        db.query(
            Capture.priority,
            func.count(Capture.id)
        )
        .group_by(Capture.priority)
        .all()
    )

    # Source Analytics

    source_stats = (
        db.query(
            Capture.source,
            func.count(Capture.id)
        )
        .group_by(Capture.source)
        .all()
    )


    return {
        "total_captures": total_captures,
        "total_plan_steps": total_plan_steps,
        "completed_steps": completed_steps,
        "pending_steps": pending_steps,
        "completion_rate": completion_rate,
        "recent_captures": [
            {
                "id": c.id,
                "text": c.original_text,
                "intent": c.intent,
                "priority": c.priority
            }
            for c in recent_captures
        ],

        "intent_distribution": [
            {
                "intent": row[0],
                "count": row[1]
            }
            for row in intent_stats
        ],

        "priority_distribution": [
            {
                "priority": row[0],
                "count": row[1]
            }
            for row in priority_stats
        ],

        "source_distribution": [
            {
                "source": row[0],
                "count": row[1]
            }
            for row in source_stats
        ]
    }

@router.get("/all-goals")
def get_all_goals(db: Session = Depends(get_db)):

    goals = db.query(Capture).all()

    return [
        {
            "id": goal.id,
            "goal": goal.original_text,
            "status": goal.status,
            "progress": goal.progress,
            "priority": goal.priority
        }
        for goal in goals
    ]

@router.get("/goal-progress/{capture_id}")
def goal_progress(
    capture_id: int,
    db: Session = Depends(get_db)
):

    capture = db.query(Capture).filter(
        Capture.id == capture_id
    ).first()

    if not capture:
        return {
            "error": "Capture not found"
        }
    total_captures = db.query(Capture).count()

    plans = db.query(ActionPlan).filter(
        ActionPlan.capture_id == capture_id
    ).all()

    total_steps = len(plans)

    completed_steps = len(
        [
            p for p in plans
            if p.status == "Completed"
        ]
    )

    pending_steps = total_steps - completed_steps

    completion_rate = 0
    status='pending'

    if total_steps > 0:

        completion_rate = round(
            (completed_steps / total_steps) * 100,
            2
        )
        

        if completion_rate == 100:
                status = "Completed"

        elif completion_rate >= 75:
                status = "Almost Complete"

        elif completion_rate >= 25:
                status = "In Progress"

    # Save progress and status to Capture table       
    capture.progress = int(completion_rate)
    capture.status = status

    db.commit()
    
    
    

    return {
        "capture_id": capture.id,
        "goal": capture.original_text,
        "total_captures": total_captures,
        "total_steps": total_steps,
        "completed_steps": completed_steps,
        "pending_steps": pending_steps,
        "completion_rate": completion_rate,
        "progress": capture.progress,
        "status": capture.status
    }

