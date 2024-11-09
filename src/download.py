import re
from pathlib import Path
from typing import Union

import yt_dlp
from loguru import logger


def sanitize_title(title: str) -> str:
    """Convert title to snake_case and remove special characters.

    Args:
        title: The original title string

    Returns:
        Sanitized title in snake_case format
    """
    # Convert to lowercase
    title = title.lower()

    # Replace special characters and spaces with underscore
    # First replace common separators with space
    title = re.sub(r"[-–—:]", " ", title)
    # Remove any other special characters
    title = re.sub(r"[^\w\s]", "", title)
    # Replace whitespace with single underscore
    title = re.sub(r"\s+", "_", title.strip())
    # Remove multiple consecutive underscores
    title = re.sub(r"_+", "_", title)

    return title


def download_audio(url: str, output_path: Union[str, Path]) -> Path:
    """Download audio from YouTube URL.

    Args:
        url: YouTube video URL
        output_path: Path to save the audio file

    Returns:
        Path to the downloaded audio file
    """
    logger.info(f"Downloading audio from: {url}")
    logger.debug(f"Output path: {output_path}")

    # First, get the info without downloading
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
        info = ydl.extract_info(url, download=False)
        original_title = info.get("title", "untitled")
        sanitized_title = sanitize_title(original_title)

    # Now download with the sanitized filename
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_path}/{sanitized_title}.%(ext)s",  # Use sanitized title here
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.debug("Starting download...")
            ydl.download([url])

            # Get the output file path
            output_file = Path(output_path) / f"{sanitized_title}.mp3"
            logger.success(f"Audio downloaded successfully: {output_file}")
            assert output_file.exists(), "Audio file not found"

            return output_file

    except Exception as e:
        logger.exception("Download failed")
        raise RuntimeError(f"Failed to download audio: {str(e)}")


if __name__ == "__main__":
    from pathlib import Path

    output_path = Path("/Users/tommylees/Downloads")
    url = "https://www.youtube.com/watch?v=DTOU3vchBE0&ab_channel=DwarkeshPatel"
    url = "https://www.youtube.com/shorts/q5HiRc93xMU"

    print(download_audio(url, output_path=output_path))
