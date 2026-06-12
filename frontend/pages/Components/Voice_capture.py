import streamlit as st
import requests

from streamlit_mic_recorder import (
    mic_recorder
)

API_URL = "http://127.0.0.1:8000"


def render_voice_capture():

    st.subheader(
        "🎤 Voice Capture"
    )

    audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
    )

    
    if audio:

        st.session_state["audio_data"] = audio

        st.success("Audio Recorded")
    if "audio_data" in st.session_state:

        if st.button(
            "Process Voice"
        ):

            audio = st.session_state[
                "audio_data"
            ]

            with open(
                "recording.wav",
                "wb"
            ) as f:

                f.write(
                    audio["bytes"]
                )

            with open(
                "recording.wav",
                "rb"
            ) as audio_file:

                files = {
                    "audio": (
                        "recording.wav",
                        audio_file,
                        "audio/wav"
                    )
                }

                response = requests.post(
                    f"{API_URL}/voice-capture",
                    files=files
                )

                result = response.json()
                transcription = result["transcription"]
    
                st.write(transcription)

            response = requests.post(
            f"{API_URL}/capture",
            json={
                "text": transcription
            })

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