import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("🧠 Memory Explorer")

query = st.text_input(
    "Search your memory"
)

if st.button("Search"):

    response = requests.get(
        f"{API_URL}/memory-search",
        params={
            "query": query
        }
    )

    st.session_state["memory_results"] = (
        response.json()["results"]
    )


if "memory_results" in st.session_state:

    results = st.session_state[
        "memory_results"
    ]

    if results:

        option_map = {
            f"[{r['intent']}] {r['text']}":
            r["capture_id"]
            for r in results
        }

        selected = st.selectbox(
            "Select Memory",
            list(option_map.keys())
        )

        capture_id = option_map[selected]

        details = requests.get(
            f"{API_URL}/memory-details/{capture_id}"
        ).json()

        st.subheader(details["text"])

        st.write(
            f"Intent: {details['intent']}"
        )

        st.write(
            f"Priority: {details['priority']}"
        )

        st.write(
            f"Status: {details['status']}"
        )

        progress = details.get(
            "progress",
            0
        )

        st.progress(progress / 100)

        st.write(
            f"{progress}% Complete"
        )

        st.write("### Action Plan")

        for plan in details["plans"]:

            st.write(
                f"{plan['step_number']}. {plan['title']}"
            )

            st.caption(
                plan["description"]
            )

            st.write(
                f"Status: {plan['status']}"
            )