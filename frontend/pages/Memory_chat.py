import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.markdown(
    "<h2 style='color:white;'>🧠 Ask Memory</h2>",
    unsafe_allow_html=True
)

st.caption(
    "Search your past activities using semantic memory."
)

query = st.text_input(
    "What are you looking for?",
    placeholder="e.g. interview, groceries, project deadline"
)

if st.button("🔍 Search Memory"):

    if not query:

        st.warning(
            "Please enter a search query."
        )

    else:

        with st.spinner(
            "Searching memories..."
        ):

            response = requests.get(
                f"{API_URL}/memory-search",
                params={
                    "query": query
                }
            )

            if response.status_code != 200:

                st.error(
                    "Unable to search memory."
                )

            else:

                results = response.json().get(
                    "results",
                    []
                )

                if not results:

                    st.info(
                        "No matching memories found."
                    )

                else:

                    st.success(
                        f"Found {len(results)} related memories"
                    )

                    for item in results:

                        with st.expander(
                            item["text"]
                        ):

                            st.write(
                                f"**Intent:** {item['intent']}"
                            )

                            # st.write(
                            #     f"**Priority:** {item['priority']}"
                            # )

                            st.write(
                                f"**Status:** {item['status']}"
                            )

                            if item.get(
                                "plans"
                            ):

                                st.write(
                                    "### Action Plan"
                                )

                                for plan in item[
                                    "plans"
                                ]:

                                    st.write(
                                        f"• {plan['step']}"
                                    )

                                    st.caption(
                                        f"Status: {plan['status']}"
                                    )

                            