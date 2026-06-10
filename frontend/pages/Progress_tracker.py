import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("🎯 Progress Tracker")

try:

    goals_response = requests.get(
        f"{API_URL}/all-goals"
    )

    if goals_response.status_code != 200:
        st.error("Unable to load goals")
        st.stop()

    goals = goals_response.json()

    if not goals:
        st.warning("No goals found")
        st.stop()

    goal_map = {
        f"{g['id']} - {g['goal']}": g["id"]
        for g in goals
    }

    selected_goal = st.selectbox(
        "Select Goal",
        list(goal_map.keys())
    )

    capture_id = goal_map[selected_goal]

    progress_data = requests.get(
        f"{API_URL}/goal-progress/{capture_id}"
    ).json()

    plans = requests.get(
        f"{API_URL}/plans/{capture_id}"
    ).json()

    st.subheader(progress_data["goal"])

    status = progress_data["status"]

    if status == "Completed":
        st.success(f"✅ {status}")

    elif status == "Almost Complete":
        st.info(f"🚀 {status}")

    elif status == "In Progress":
        st.warning(f"⏳ {status}")

    else:
        st.error(f"⭕ {status}")

    progress = progress_data["progress"]

    st.progress(progress / 100)

    st.write(
        f"### {progress}% Complete"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Total Steps",
            progress_data["total_steps"]
        )

    with c2:
        st.metric(
            "Completed",
            progress_data["completed_steps"]
        )

    with c3:
        st.metric(
            "Pending",
            progress_data["pending_steps"]
        )

    st.divider()

    st.subheader("Plan Steps")

    if isinstance(plans, dict):

        st.error(plans.get("detail", "No plans found"))
        st.stop()

    for step in plans:

        completed = (
            step["status"] == "Completed"
        )

        checked = st.checkbox(
            f"Step {step['step_number']} - {step['step_title']}",
            value=completed,
            key=f"step_{step['id']}"
        )

        st.caption(
            step["step_description"]
        )

        if checked != completed:

            requests.put(
                f"{API_URL}/plan-step/{step['id']}",
                json={
                    "status":
                    "Completed"
                    if checked
                    else "Pending"
                }
            )

            st.rerun()

except Exception as e:

    st.error(
        f"Error: {str(e)}"
    )