import os
import tempfile
from pathlib import Path

import click

from download import download_audio
from transcribe import transcribe_audio


@click.command()
@click.argument("url")
@click.option(
    "--output",
    "-o",
    help="Output file path for the transcript",
    default="transcript.txt",
)
@click.option(
    "--keep-audio/--no-keep-audio",
    help="Keep the downloaded audio file",
    default=False,
)
def main(url, output, keep_audio):
    """Convert YouTube videos to text transcripts.

    URL: The YouTube video URL to transcribe
    """
    # Create a temporary directory that gets cleaned up automatically
    with tempfile.TemporaryDirectory() as temp_dir:
        click.echo(f"Downloading video from: {url}")
        # Use temp_dir for audio file
        audio_path = Path(temp_dir) / "audio.mp3"
        download_audio(url, output_path=audio_path)

        click.echo("Transcribing audio...")
        transcript = transcribe_audio(audio_path)

        # Save transcript to file
        with open(output, "w") as f:
            f.write(transcript)

        # Optionally save the audio file
        if keep_audio:
            final_audio = Path(output).with_suffix(".mp3")
            os.replace(audio_path, final_audio)
            click.echo(f"Audio saved to: {final_audio}")

    click.echo(f"Transcript saved to: {output}")


if __name__ == "__main__":
    main()
