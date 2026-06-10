import streamlit as st
import speech_recognition as sr
import requests

API_URL = "http://127.0.0.1:8000"

st.title("🎤 Voice Capture")

if st.button("Start Recording"):

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            st.info("Listening...")

            audio = recognizer.listen(
                source,
                timeout=10
            )

        text = recognizer.recognize_google(
            audio
        )

        st.success(
            f"Recognized: {text}"
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
                "Capture Saved"
            )

            st.json(result)

        else:

            st.error(
                response.text
            )

    except Exception as e:

        st.error(
            str(e)
        )