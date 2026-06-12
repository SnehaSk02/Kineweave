import streamlit as st
import requests
from datetime import date

API_URL = "http://127.0.0.1:8000"

st.markdown("<h2 style='color: white;'>📅 Daily AI Summary</h2>", unsafe_allow_html=True)
st.caption("Deep dive into a specific date.")

# Date Picker
selected_date = st.date_input("Select Date", value=date.today())
formatted_date = selected_date.strftime("%Y-%m-%d")

try:
    response = requests.get(f"{API_URL}/daily-summary", params={"date": formatted_date})
    
    if response.status_code == 200:
        data = response.json()

        # Metrics specific to this date
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Completion Rate", f"{data.get('completion_rate', 0)}%")
        with c2:
            st.metric("Pending Tasks", data.get('pending_tasks', 0))

        st.markdown("---")

        col1, col2 = st.columns([2, 1])

        with col1:
            # AI Summary
            st.write("#### 🤖 AI Overview")
            st.markdown(f"""
            <div style="background-color: #1E1E24; padding: 15px; border-radius: 10px; color: #B9B9B9; border: 1px solid #FF6B6B;">
                {data.get('summary', 'No summary available.')}
            </div>
            """, unsafe_allow_html=True)
            
            # Pending Tasks with Steps
            st.write("#### ⏳ Pending Tasks Breakdown")
            pending_list = data.get('pending_tasks_list', [])
            
            if pending_list:
                for task in pending_list:
                    with st.expander(f"**{task['text']}** ({task['priority']})", expanded=False):
                        st.write(f"**Progress:** {task['progress']}%")
                        if task['steps']:
                            for step in task['steps']:
                                check = "✅" if step['status'] == "Completed" else "⬜"
                                st.write(f"{check} {step['title']}")
            else:
                st.success("No pending tasks for this date.")

        with col2:
            # Stats Card
            st.write("#### 📈 Stats")
            st.markdown(f"""
            <div style="background-color: #1E1E24; padding: 15px; border-radius: 10px;">
                <p><strong>Total Created:</strong> {data.get('total_tasks', 0)}</p>
                <p><strong>High Priority:</strong> {data.get('high_priority', 0)}</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.error("Could not load summary.")

except Exception as e:
    st.error(f"Error: {e}")