import os
import tempfile
import warnings
from pathlib import Path
from typing import Optional

import click

from src.download import download_audio
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
    with tempfile.TemporaryDirectory() as temp_dir:
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
            output = audio_path.stem
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
