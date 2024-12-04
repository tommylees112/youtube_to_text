from typing import Optional

import click
from loguru import logger
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._transcripts import TranscriptsDisabled

from src.format_transcript import format_transcript


@click.command()
@click.argument("url")
def extract_transcript(url: str) -> Optional[str]:
    video_id = url.split("v=")[1]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except TranscriptsDisabled:
        logger.info(
            "Transcripts are disabled for this video. Reverting to download audio and whisper convert."
        )
        return

    # iterate through segments and create an 'end' key with the 'start' + 'duration'
    for segment in transcript:
        segment["end"] = segment["start"] + segment["duration"]

    formatted_transcript = format_transcript(transcript)
    print(formatted_transcript)


if __name__ == "__main__":
    url = "https://www.youtube.com/watch\?v\=Td_PGkfIdIQ\&t\=2s\&ab_channel\=blogphilofilms"
    url = "https://www.youtube.com/watch?v=dpCSr9jkOic&ab_channel=Savotta"
    extract_transcript()
