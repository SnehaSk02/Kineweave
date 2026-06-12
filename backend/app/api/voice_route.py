from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import tempfile
import os

from app.services.speech_service import (
    transcribe_audio
)

router = APIRouter()


@router.post("/voice-capture")
async def voice_capture(
    audio: UploadFile = File(...)
):
    print("Voice request received")

    suffix = os.path.splitext(
        audio.filename
    )[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as tmp:

        content = await audio.read()

        tmp.write(content)

        temp_path = tmp.name

    try:

        text = transcribe_audio(
            temp_path
        )

        return {
            "transcription": text
        }

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)