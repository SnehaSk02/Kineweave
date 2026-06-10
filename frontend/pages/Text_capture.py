import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Text Capture")

text = st.text_area(
    "Enter your thought"
)

if st.button("Analyze"):

    response = requests.post(
        f"{API_URL}/capture",
        json={
            "text": text
        }
    )

    st.json(
        response.json()
    )