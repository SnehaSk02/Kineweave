import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def render_form_capture():

    st.subheader(
        "📋 Form Capture"
    )

    title = st.text_input(
        "Title"
    )

    due_date = st.date_input(
        "Due Date"
    )

    priority = st.selectbox(
        "Priority",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    if st.button(
        "Submit Form",
        key="form_capture_btn"
    ):

        if not title:

            st.warning(
                "Please enter a goal."
            )

            return

        due_date_str = due_date.strftime("%Y-%m-%d")

        text = (
            f"{title}. "
            f"Due on {due_date_str}. "
            f"Priority is {priority}."
        )

        response = requests.post(
            f"{API_URL}/capture",
            json={
                "text": title,
                "deadline":due_date_str,
                "priority":priority
            }
        )

        if response.status_code == 200:

            result = response.json()

            st.success(
                "Task Captured Successfully"
            )

            for capture in result.get(
                "captures",
                []
            ):

                with st.expander(
                    capture["text"]
                ):

                    st.write(
                        f"Intent: "
                        f"{capture['intent']}"
                    )

                    st.write(
                        f"Priority: "
                        f"{priority}"
                    )

                    st.write(
                        f"Due_date: "
                        f"{capture.get('deadline', 'No deadline')}")

        else:

            st.error(
                "Capture Failed"
            )