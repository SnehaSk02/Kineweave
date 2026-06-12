import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.markdown("<h2 style='color: white;'>📈 Progress Tracker</h2>", unsafe_allow_html=True)
st.caption("Select a task to track its completion.")

try:
    # 1. Fetch all goals
    goals_response = requests.get(f"{API_URL}/all-goals")

    if goals_response.status_code != 200:
        st.error("Unable to load goals")
        st.stop()

    goals = goals_response.json()

    if not goals:
        st.warning("No goals found. Add a task first!")
        st.stop()

    # 2. Select a Task (Using ID ensures the selection remains stable even if text changes)
    goal_map = {
        f"{g['id']} - {g['goal']}": g["id"]
        for g in goals
    }

    selected_label = st.selectbox("Select Goal", list(goal_map.keys()))
    capture_id = goal_map[selected_label]

    # 3. Fetch Detailed Progress Data (Includes specific status text and counts)
    progress_data = requests.get(f"{API_URL}/goal-progress/{capture_id}").json()
    
    # 4. Fetch Action Plan Steps
    plans_response = requests.get(f"{API_URL}/plans/{capture_id}")
    
    # Handle case where plans endpoint returns an error dict
    if isinstance(plans_response.json(), dict):
        st.error(plans_response.json().get("detail", "No plans found"))
        plans = []
    else:
        plans = plans_response.json()

    # --- UI SECTION ---

    # Task Title & Status
    st.subheader(progress_data["goal"])
    status = progress_data["status"]

    # Color-coded Status Badges
    if status == "Completed":
        st.success(f"✅ Status: {status}")
    elif status == "Almost Complete":
        st.info(f"🚀 Status: {status}")
    elif status == "In Progress":
        st.warning(f"⏳ Status: {status}")
    else:
        st.error(f"⭕ Status: {status}")

    # Progress Bar
    progress = progress_data["progress"]
    st.progress(progress / 100)
    st.write(f"### {progress}% Complete")

    # Detailed Metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Steps", progress_data["total_steps"])
    with c2:
        st.metric("Completed", progress_data["completed_steps"])
    with c3:
        st.metric("Pending", progress_data["pending_steps"])

    st.divider()

    # --- INTERACTIVE CHECKLIST ---
    st.subheader("Action Plan Steps")

    if not plans:
        st.info("No steps generated for this task yet.")
    
    for step in plans:
        # Determine checked state
        is_completed = step["status"] == "Completed"

        # Display Checkbox with Description
        checked = st.checkbox(
            f"**Step {step['step_number']}:** {step['step_title']}", 
            value=is_completed, 
            key=f"step_{step['id']}"
        )
        
        if step.get("step_description"):
            st.caption(step["step_description"])

        # --- UPDATE LOGIC ---
        new_status = "Completed" if checked else "Pending"

        if new_status != step["status"]:
            # Status changed! Send Update
            try:
                # Using toast for non-blocking feedback
                with st.spinner("Updating..."):
                    update_resp = requests.put(
                        f"{API_URL}/plan-step/{step['id']}",
                        json={"status": new_status}
                    )

                if update_resp.status_code == 200:
                    # Show a quick success message
                    st.toast("Status updated!", icon="✅")
                    # Rerun to refresh progress bar and parent status
                    st.rerun()
                else:
                    st.error("Failed to update status.")

            except Exception as e:
                st.error(f"Error updating step: {e}")

except Exception as e:
    st.error(f"An unexpected error occurred: {e}")