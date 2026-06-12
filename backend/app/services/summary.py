from sqlalchemy import func
from app.models.capture import Capture
from app.models.action_plan import ActionPlan

from app.services.llm_service import ask_llm

def generate_daily_summary(db,target_date=None):
    base_query = db.query(Capture)
    # If a date is provided, filter the base query by the created_at date
    if target_date:
        base_query = base_query.filter(func.date(Capture.created_at) == target_date)

    captures = base_query.all()
    #fetch pending tasks
    pending = base_query.filter(
        Capture.status != "Completed"
    ).all()
    #fetch high priority tasks
    high_priority = base_query.filter(
        Capture.priority == "High"
    ).all()

    capture_ids = [c.id for c in captures] #to get capture_ids of items in captures
        
    #progress stats
    total_steps = db.query(ActionPlan).filter(
        ActionPlan.capture_id.in_(capture_ids)
    ).count()

    completed_steps = db.query(ActionPlan).filter(
        ActionPlan.capture_id.in_(capture_ids),
        ActionPlan.status == "Completed"
        ).count()

    completion_rate = 0

    if total_steps:

        completion_rate = round(
            (completed_steps /
                total_steps) * 100,
                2
            )

        #context
    context = f"""
    Date: {target_date if target_date else 'All Time'}
    
    Pending Items (on this date):
    {[c.original_text for c in pending]}

    High Priority (on this date):
    {[c.original_text for c in high_priority]}

    Progress:
    {completed_steps}/{total_steps} steps completed for tasks created on this date.

    Completion Rate:
    {completion_rate}%
            """
        
        #prompt
    prompt = f"""
                You are a productivity assistant.

    Generate a concise daily summary based on the context provided.

    Context:
    {context}

    Return plain text.
    """
        
    try:
        summary_text = ask_llm(prompt)
    except Exception:
        summary_text = "Could not generate AI summary at this time."

    pending_tasks_data = []
    for task in pending:
        # Fetch steps for this specific task
        steps = db.query(ActionPlan).filter(ActionPlan.capture_id == task.id).all()
        
        pending_tasks_data.append({
            "id": task.id,
            "text": task.original_text,
            "intent": task.intent,
            "priority": task.priority,
            "progress": task.progress,
            "steps": [
                {
                    "step_number": s.step_number,
                    "title": s.step_title,
                    "description": s.step_description,
                    "status": s.status
                }
                for s in steps
            ]
        })

    return {
        "summary": summary_text,
        "date": str(target_date) if target_date else "All Time",
        "total_tasks": len(captures),
        "pending_tasks": len(pending),
        "high_priority": len(high_priority),
        "completion_rate": completion_rate,
        "pending_tasks_list": pending_tasks_data

    }
