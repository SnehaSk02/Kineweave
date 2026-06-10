import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("📋 Form Capture")

goal = st.text_input(
    "Goal"
)

deadline = st.date_input(
    "Deadline"
)

priority = st.selectbox(
    "Priority",
    [
        "Low",
        "Medium",
        "High"
    ]
)

if st.button("Create Goal"):

    payload = {
        "text": goal,
        "deadline": str(deadline),
        "priority": priority,
        "source": "form"
    }

    response = requests.post(
        f"{API_URL}/capture",
        json=payload
    )

    if response.status_code == 200:

        st.success(
            "Goal Saved"
        )

        st.json(
            response.json()
        )

    else:

        st.error(
            response.text
        )