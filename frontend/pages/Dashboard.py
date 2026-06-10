import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def fetch_dashboard_data():
    try:
        response = requests.get(f"{API_URL}/dashboard")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
    return None

def fetch_all_goals():
    try:
        response = requests.get(f"{API_URL}/all-goals")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error fetching goals: {e}")
    return []

st.set_page_config(page_title="KineWeave Dashboard", layout="wide")

st.title("🚀 KineWeave Productivity Dashboard")

# Refresh Button
if st.button("Refresh Dashboard"):
    st.cache_data.clear()
    st.rerun()

# --- 1. TOP METRICS SECTION ---
dashboard_data = fetch_dashboard_data()

if dashboard_data:
    m1, m2, m3, m4 = st.columns(4)
    
    m1.metric("Total Captures", dashboard_data.get("total_captures", 0))
    m2.metric("Completion Rate", f"{dashboard_data.get('completion_rate', 0)}%")
    m3.metric("Completed Steps", dashboard_data.get("completed_steps", 0))
    m4.metric("Pending Steps", dashboard_data.get("pending_steps", 0))

# --- 2. MAIN PRIORITY BOARD ---
st.markdown("---")
st.header("🎯 Active Goals & Tasks")

all_goals = fetch_all_goals()

# Define Columns based on Priority
col_high, col_med, col_low = st.columns(3)

# Helper to render a single goal card
def render_goal_card(goal):
    """
    Renders a single goal with progress bar and status.
    """
    # Logic to determine color/status styling
    status = goal.get('status', 'Unknown')
    progress = goal.get('progress', 0)
    
    # Visual cues for status
    status_emoji = "🔴"
    if status == "Completed": status_emoji = "✅"
    elif status == "In Progress": status_emoji = "🟡"
    elif status == "Almost Complete": status_emoji = "🟠"
    
    # We use an expander for a clean UI that can be expanded to see details
    with st.expander(f"{status_emoji} **{goal['goal']}** ({progress}%)"):
        
        # 1. Progress Bar
        st.progress(progress)
        
        # 2. Status Display
        st.caption(f"**Current Status:** {status}")
        
    #     # 3. Interactive Area (The "Steps" Simulation)
    #     # NOTE: Your current API endpoints return counts, not the list of step objects.
    #     # To make the checkboxes fully functional, you would need a new endpoint 
    #     # like /get-steps/{capture_id} that returns the list of steps.
    #     # Below is a simulation of how that would look:
        
    #     st.markdown("**Sub-steps:**")
        
    #     # Mocking steps for visual demonstration based on progress
    #     # In production: steps = fetch_steps(goal['id'])
    #     total_mock_steps = 5
    #     completed_mock_steps = int((progress / 100) * total_mock_steps)
        
    #     for i in range(total_mock_steps):
    #         is_checked = i < completed_mock_steps
    #         # The key ensures unique checkboxes
    #         checkbox_label = f"Step {i+1}: Sub-task for {goal['goal']}"
    #         st.checkbox(checkbox_label, value=is_checked, key=f"{goal['id']}_step_{i}", disabled=True)

    #     # Action Button
    #     if st.button(f"Update Progress for ID {goal['id']}", key=f"btn_{goal['id']}"):
    #         # Trigger your update logic here
    #         st.success("Progress updated!")

# --- POPULATE COLUMNS ---

# Column 1: High Priority
with col_high:
    st.markdown("### 🔴 High Priority")
    high_goals = [g for g in all_goals if g.get('priority') == 'High']
    
    if not high_goals:
        st.info("No High Priority tasks.")
    else:
        for goal in high_goals:
            render_goal_card(goal)

# Column 2: Medium Priority
with col_med:
    st.markdown("### 🟠 Medium Priority")
    med_goals = [g for g in all_goals if g.get('priority') == 'Medium']
    
    if not med_goals:
        st.info("No Medium Priority tasks.")
    else:
        for goal in med_goals:
            render_goal_card(goal)

# Column 3: Low Priority
with col_low:
    st.markdown("### 🟢 Low Priority")
    low_goals = [g for g in all_goals if g.get('priority') == 'Low']
    
    if not low_goals:
        st.info("No Low Priority tasks.")
    else:
        for goal in low_goals:
            render_goal_card(goal)
 