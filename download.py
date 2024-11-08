from pathlib import Path
from typing import Union

import yt_dlp
from loguru import logger


def download_audio(url: str, output_path: Union[str, Path]) -> Path:
    logger.info(f"Downloading audio from: {url}")
    logger.debug(f"Output path: {output_path}")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path


if __name__ == "__main__":
    from pathlib import Path

    output_path = Path("/Users/tommylees/Downloads")
    url = "https://www.youtube.com/watch?v=DTOU3vchBE0&ab_channel=DwarkeshPatel"

    print(download_audio(url, output_path=output_path))
