import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def render_text_capture():

    st.subheader(
        "📝 Text Capture"
    )

    text = st.text_area(
        "Enter your task"
    )

    if st.button(
        "Capture Text",
        key="text_capture_btn"
    ):

        response = requests.post(
            f"{API_URL}/capture",
            json={
                "text": text
            }
        )

        if response.status_code == 200:

            st.success(
                "Task Captured"
            )

            st.json(
                response.json()
            )

        else:

            st.error(
                "Capture failed"
            )