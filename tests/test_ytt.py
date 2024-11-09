from pathlib import Path
from unittest.mock import patch

import pytest

from tests.segments import TEST_SEGMENTS
from ytt import get_downloads_dir, main


def test_get_downloads_dir():
    downloads = get_downloads_dir()
    assert isinstance(downloads, Path)
    assert downloads.name == "Downloads"


@pytest.fixture
def mock_dependencies():
    # mock 3 dependencies: download_audio, transcribe_audio, format_transcript
    with patch("src.download.download_audio") as mock_download, patch(
        "src.transcribe.transcribe_audio"
    ) as mock_transcribe, patch(
        "src.format_transcript.format_transcript"
    ) as mock_format:
        # Setup mock returns
        mock_download.return_value = Path("/tmp/test.mp3")
        mock_transcribe.return_value = {
            "text": "Test transcription",
            "segments": TEST_SEGMENTS,
        }
        mock_format.return_value = "Formatted transcript"

        yield {
            "download": mock_download,
            "transcribe": mock_transcribe,
            "format": mock_format,
        }


@pytest.mark.slow
@pytest.mark.integration
def test_main_with_timestamps(mock_dependencies, tmp_path):
    # Test the main function with timestamps
    from click.testing import CliRunner

    runner = CliRunner()
    with patch("click.echo"):
        result = runner.invoke(
            main,
            [
                "https://youtube.com/test",
                "--output",
                "test.txt",
                "--no-keep-audio",
                "--output-dir",
                str(tmp_path),
                "--with-timestamps",
            ],
        )
    assert result.exit_code == 0


@pytest.mark.slow
@pytest.mark.integration
def test_main_without_timestamps(mock_dependencies, tmp_path):
    # Test the main function without timestamps
    from click.testing import CliRunner

    runner = CliRunner()
    with patch("click.echo"):
        result = runner.invoke(
            main,
            [
                "https://youtube.com/test",
                "--output",
                "test.txt",
                "--no-keep-audio",
                "--output-dir",
                str(tmp_path),
                "--no-timestamps",
            ],
        )
    assert result.exit_code == 0
