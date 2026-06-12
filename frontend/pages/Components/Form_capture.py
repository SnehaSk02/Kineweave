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

        text = (
            f"{title}. "
            f"Due on {due_date}. "
            f"Priority is {priority}."
        )

        response = requests.post(
            f"{API_URL}/capture",
            json={
                "text": text
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
                        f"{capture['priority']}"
                    )

                    st.write(
                        f"Steps Created: "
                        f"{capture['steps_created']}"
                    )

        else:

            st.error(
                "Capture Failed"
            )