from difflib import SequenceMatcher
from pathlib import Path

import pytest

from src.transcribe import transcribe_audio


@pytest.mark.slow
@pytest.mark.integration
def test_transcribe_audio_basic():
    test_audio_file = Path(__file__).parent / "audio.mp3"
    result = transcribe_audio(test_audio_file, model_str="turbo")

    # Check the structure of the result
    assert isinstance(result, dict)
    assert "text" in result
    assert "segments" in result
    assert isinstance(result["segments"], list)

    # Check segments format
    for segment in result["segments"]:
        assert "text" in segment
        assert "start" in segment
        assert "end" in segment

    # check the text
    actual = result["text"]
    expected = "the probability is iterated over many years and decades. Right, yeah. You've got to always not use nuclear weapons, right? Pandora has already, the box has been opened, the nukes are there."

    # Option 1: Check key phrases exist
    key_phrases = ["probabilit", "nuclear weapons", "nukes", "decades"]
    for phrase in key_phrases:
        assert (
            phrase.lower() in actual.lower()
        ), f"Expected to find '{phrase}' in transcribed text"

    # Option 2: Check similarity
    similarity = SequenceMatcher(None, expected.lower(), actual.lower()).ratio()
    assert similarity > 0.8, f"Text similarity {similarity} is below threshold"


def test_transcribe_audio_invalid_file():
    with pytest.raises(Exception):
        transcribe_audio(Path("nonexistent.mp3"))
