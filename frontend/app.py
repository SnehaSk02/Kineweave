import streamlit as st

st.set_page_config(
    page_title="KineWeave",
    page_icon="🌞",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    """
    # 🦁 KineWeave
    AI Productivity Assistant
    """
)

with st.sidebar:
    if st.page_link("app.py", label="🌞 KineWeave", use_container_width=True):
        pass
    st.markdown("---")
    st.markdown("### 🗂️ Menu")
    st.page_link("pages/add_task.py", label="➕ Add Task", icon=":material/add_circle:")
    st.page_link("pages/Progress_tracker.py", label="📈 Progress Tracker", icon=":material/bar_chart:")
    st.page_link("pages/Dashboard.py", label="📊 Dashboard", icon=":material/dashboard:")
    st.page_link("pages/Daily_summary.py", label="📅 Daily Summary", icon=":material/calendar_today:")
    st.page_link("pages/Memory_chat.py", label="🧠 Ask Memory", icon=":material/history:")

    st.markdown("---")
    st.caption("Designed for Productivity")

# Welcome Page Content
st.markdown('<h1 class="hero-title">Welcome Back, Sneha</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Your personal AI-powered productivity assistant is ready.</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""<div class="metric-card"><h3>📊 View Dashboard</h3><p>Global stats and overview.</p></div>""", unsafe_allow_html=True)
    if st.button("Go to Dashboard", type="primary", use_container_width=True): st.switch_page("pages/Dashboard.py")

with col2:
    st.markdown("""<div class="metric-card"><h3>📅 Daily Summary</h3><p>AI analysis for specific dates.</p></div>""", unsafe_allow_html=True)
    if st.button("Daily Summary", use_container_width=True): st.switch_page("pages/Daily_summary.py")

with col3:
    st.markdown("""<div class="metric-card"><h3>➕ Add Task</h3><p>Capture new thoughts.</p></div>""", unsafe_allow_html=True)
    if st.button("Add Task", use_container_width=True): st.switch_page("pages/add_task.py")

