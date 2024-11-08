from pathlib import Path
from typing import Literal

import whisper
from loguru import logger


def transcribe_audio(
    audio_file: Path, model: Literal["base", "turbo"] = "turbo"
) -> list[dict]:
    logger.info(f"Loading Whisper {model} model...")
    model = whisper.load_model(model)

    logger.info(f"Starting transcription of: {audio_file}")
    try:
        result = model.transcribe(audio_file, word_timestamps=True)
        logger.success("Transcription completed successfully")
        return result["segments"]
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        raise


if __name__ == "__main__":
    from pathlib import Path

    audio_file = Path(
        "/Users/tommylees/Downloads/Taiwan Invasion： Timeline to Global Collapse – @Asianometry & Dylan Patel.mp3"
    )
    assert audio_file.exists(), logger.error(f"Audio file not found: {audio_file}")

    transcribe_audio(audio_file, model="base")
