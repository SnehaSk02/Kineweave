import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.markdown("<h2 style='color: white;'>📊 Global Dashboard</h2>", unsafe_allow_html=True)
st.caption("Overview of all your tasks across all time.")

# Fetch all goals to calculate global stats
try:
    response = requests.get(f"{API_URL}/all-goals")
    
    if response.status_code == 200:
        goals = response.json()
        
        # Calculate Stats
        total_tasks = len(goals)
        pending_tasks = len([g for g in goals if g['status'] != 'Completed'])
        completed_tasks = len([g for g in goals if g['status'] == 'Completed'])
        high_priority = len([g for g in goals if g['priority'] == 'High'])

        # Metric Cards
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown(f"""<div class="metric-card"><h3 style="color: #4D96FF;">TOTAL</h3><p style="font-size: 24px;">{total_tasks}</p></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="metric-card"><h3 style="color: #FF6B6B;">PENDING</h3><p style="font-size: 24px;">{pending_tasks}</p></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="metric-card"><h3 style="color: #6BCB77;">COMPLETED</h3><p style="font-size: 24px;">{completed_tasks}</p></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="metric-card"><h3 style="color: #FFD93D;">HIGH PRIORITY</h3><p style="font-size: 24px;">{high_priority}</p></div>""", unsafe_allow_html=True)

        st.markdown("---")
        
        # High Priority List
        st.write("#### 🔥 High Priority Tasks")
        high_priority_goals = [g for g in goals if g['priority'] == 'High' and g['status'] != 'Completed']
        
        if high_priority_goals:
            for goal in high_priority_goals:
                st.markdown(f"""
                <div style="background-color: #1E1E24; padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #FF6B6B;">
                    <strong>{goal['goal']}</strong><br>
                    <small style="color: #B9B9B9;">Progress: {goal['progress']}%</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No high priority tasks pending!")
            
        # Recent Tasks
        st.write("#### 🕒 Recently Added")
        # Show last 5 tasks
        recent = goals[-5:] if len(goals) > 5 else goals
        for goal in reversed(recent):
            status_icon = "✅" if goal['status'] == 'Completed' else "⬜"
            st.write(f"{status_icon} **{goal['goal']}** ({goal['priority']})")

    else:
        st.error("Could not load dashboard data.")

except Exception as e:
    st.error(f"Error: {e}")