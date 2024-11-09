from unittest.mock import MagicMock, patch

import pytest
from yt_dlp.utils import DownloadError

from src.download import download_audio, sanitize_title


def test_sanitize_title():
    test_cases = [
        ("Normal Title", "normal_title"),
        ("Title - With Dashes", "title_with_dashes"),
        ("Special!@#$Characters", "specialcharacters"),
        ("Multiple   Spaces", "multiple_spaces"),
        ("Mixed-Case_TITLE", "mixed_case_title"),
        ("Title with — em dash", "title_with_em_dash"),
    ]

    for input_title, expected in test_cases:
        assert sanitize_title(input_title) == expected


@pytest.fixture
def mock_yt_dlp():
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        # Mock the extract_info method
        mock_instance = MagicMock()
        mock_instance.extract_info.return_value = {"title": "Test Video"}
        mock_ydl.return_value.__enter__.return_value = mock_instance
        yield mock_ydl


def test_download_audio_success(mock_yt_dlp, tmp_path):
    url = "https://www.youtube.com/watch?v=test"
    expected_output = tmp_path / "test_video.mp3"

    # Create a dummy file to simulate successful download
    expected_output.touch()

    result = download_audio(url, tmp_path)
    assert result == expected_output
    assert result.exists()


def test_download_audio_failure():
    url = "https://www.youtube.com/watch?v=test"

    with pytest.raises(DownloadError, match="Incomplete YouTube ID"):
        download_audio(url, "/fake/path")
