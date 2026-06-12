import streamlit as st
from pages.Components.Text_capture import render_text_capture
from pages.Components.Voice_capture import render_voice_capture
from pages.Components.Form_capture import render_form_capture

st.set_page_config(
    page_title="Add Task",
    page_icon="➕",
    layout="wide"
)

st.title("➕ Add Task")

st.caption(
    "Capture tasks using text, voice, or forms."
)

tab1, tab2, tab3 = st.tabs(
    [
        "📝 Text Capture",
        "🎤 Voice Capture",
        "📋 Form Capture"
    ]
)

with tab1:

    render_text_capture()

with tab2:

    render_voice_capture()

with tab3:

    render_form_capture()