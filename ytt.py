import os
import tempfile
import warnings
from pathlib import Path
from typing import Optional

import click
from loguru import logger
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._transcripts import TranscriptsDisabled

from src.download import download_audio, get_video_title
from src.format_transcript import format_transcript
from src.transcribe import transcribe_audio


def get_downloads_dir():
    """Get the default Downloads directory for the current OS."""
    if os.name == "nt":  # Windows
        return Path.home() / "Downloads"
    elif os.name == "posix":  # macOS and Linux
        return Path.home() / "Downloads"
    else:
        raise OSError(f"Unsupported operating system: {os.name}")


def extract_transcript(url: str) -> Optional[dict]:
    # Extract video_id from various YouTube URL formats
    if "v=" in url:
        video_id = url.split("v=")[1].split("&")[0]  # Handle URL parameters
    elif "shorts/" in url:
        video_id = url.split("shorts/")[1].split("?")[0]  # Handle shorts URLs
    else:
        logger.error(f"Could not extract video ID from URL: {url}")
        return None

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except TranscriptsDisabled:
        logger.info(
            "Transcripts are disabled for this video. Reverting to download audio and whisper convert."
        )
        return None
    except Exception as e:
        logger.error(f"Failed to get transcript for video {video_id}: {e}")
        return None

    # Convert YouTube transcript format to match Whisper format
    formatted_segments = []
    full_text = []

    for segment in transcript:
        formatted_segments.append(
            {
                "start": segment["start"],
                "end": segment["start"] + segment["duration"],
                "text": segment["text"],
            }
        )
        full_text.append(segment["text"])

    return {
        "segments": formatted_segments,
        "text": " ".join(full_text),
        "language": "en",  # YouTube transcripts are usually in the video's language
    }


@click.command()
@click.argument("url")
@click.option(
    "--output",
    "-o",
    help="Output file path for the transcript",
    default=None,
    nargs="?",
)
@click.option(
    "--keep-audio/--no-keep-audio",
    help="Keep the downloaded audio file",
    default=False,
)
@click.option(
    "--output-dir",
    "-d",
    help="Output directory for the transcript",
    default=get_downloads_dir(),
)
@click.option(
    "--with-timestamps/--no-timestamps",
    help="Save the transcript with timestamps",
    default=True,
)
def main(
    url: str,
    output: Optional[str] = None,
    keep_audio: bool = False,
    output_dir: Path = get_downloads_dir(),
    with_timestamps: bool = True,
) -> None:
    """Convert YouTube videos to text transcripts.

    URL: The YouTube video URL to transcribe
    """
    # First try to extract existing transcript
    if "v=" in url:
        transcript = extract_transcript(url)
    else:
        transcript = None

    if transcript is None:
        # Fall back to audio download and whisper conversion
        with tempfile.TemporaryDirectory() as temp_dir:
            # ENSURE that this is all done INSIDE the temp_dir context. cleanup is automatic after the with block
            click.echo(f"Downloading video from: {url}")
            audio_path = download_audio(url, output_path=temp_dir)

            assert audio_path.exists(), "Audio file not found"
            click.echo(f"Downloaded audio to: {audio_path}")

            click.echo("Transcribing audio...")
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=FutureWarning)
                transcript = transcribe_audio(audio_path)

    # Format the transcript with timestamps if requested
    if with_timestamps:
        transcript_text = format_transcript(transcript["segments"])
    else:
        transcript_text = transcript["text"]

    # get title if output is None
    if output is None:
        # get the title from audio_path
        output = get_video_title(url)
        output += ".txt"

    # Save transcript to file
    output_fpath = Path(output_dir) / output

    with open(output_fpath, "w") as f:
        f.write(transcript_text)

    # Optionally save the audio file
    if keep_audio:
        downloads_dir = Path.home() / "Downloads"
        final_audio = downloads_dir / audio_path.name
        os.replace(audio_path, final_audio)
        click.echo(f"Audio saved to: {final_audio}")

    click.echo(f"Transcript saved to: {output_fpath}")


if __name__ == "__main__":
    main()
