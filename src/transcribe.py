from pathlib import Path
from typing import Any, Literal

import whisper
from loguru import logger


def transcribe_audio(
    audio_file: Path,
    model_str: Literal["base", "turbo"] = "turbo",
    kwargs: dict[str, Any] = {},
) -> list[dict]:
    """Transcribe an audio file using the Whisper model.

    Args:
        audio_file (Path): The path to the audio file to transcribe.
        model_str (Literal["base", "turbo"], optional): The model to use for transcription. Defaults to "turbo".
        kwargs (dict[str, Any], optional): Additional keyword arguments to pass to the Whisper model .transcribe() method.

    Returns:
        list[dict]: The transcription result. Three keys: "segments", "text", and "language".
    """
    logger.info(f"Loading Whisper {model_str} model...")
    model = whisper.load_model(model_str)

    logger.info(f"Starting transcription of: {audio_file}")
    try:
        result = model.transcribe(
            audio_file.as_posix(),
            word_timestamps=True,
            verbose=True,
            language="en",
            **kwargs,
        )
        logger.success("Transcription completed successfully")
        return result

    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        raise


if __name__ == "__main__":
    from pathlib import Path

    audio_file = Path(
        "/Users/tommylees/Downloads/could_the_war_in_ukraine_escalate_into_a_world_war.mp3"
    )
    assert audio_file.exists(), logger.error(f"Audio file not found: {audio_file}")

    transcribe_audio(audio_file, model="base")
