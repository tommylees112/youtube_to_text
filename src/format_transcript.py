import click


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def format_transcript(segments: dict, timestamps: bool = True) -> str:
    """Format the transcript with optional timestamps.

    Args:
        segments: List of transcript segments
            {"start": float, "end": float, "text": str}
        timestamps: If True, include timestamps. If False, return plain text.

    Returns:
        Formatted transcript as string
    """
    if timestamps:
        # Format with timestamps
        formatted_transcript = ""
        for segment in segments:
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            text = segment["text"].strip()
            formatted_transcript += f"[{start_time} -> {end_time}] {text}\n"
    else:
        # Format as continuous text
        formatted_transcript = " ".join(segment["text"].strip() for segment in segments)
        # Clean up any double spaces
        formatted_transcript = " ".join(formatted_transcript.split())
        formatted_transcript += "\n"

    return formatted_transcript


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    help="Output file path for the formatted transcript",
    default=None,
)
@click.option(
    "--with-timestamps/--no-timestamps",
    help="Include timestamps in the output",
    default=False,
)
def cli(input_file, output, with_timestamps):
    """Format a transcript file with optional timestamps.

    INPUT_FILE: Path to the input transcript file (txt format)
    """
    from pathlib import Path

    # Read the input file
    with open(input_file, "r") as f:
        text = f.read()

    # Parse the text into segments
    segments = []
    for line in text.strip().split("\n"):
        if line.startswith("["):
            # Extract timestamp and text
            timestamp_part, text_part = line.split("]", 1)
            start_str, end_str = timestamp_part[1:].split(" -> ")

            # Convert timestamps to seconds
            def time_to_seconds(time_str):
                h, m, s = map(int, time_str.split(":"))
                return h * 3600 + m * 60 + s

            segments.append(
                {
                    "start": time_to_seconds(start_str),
                    "end": time_to_seconds(end_str),
                    "text": text_part.strip(),
                }
            )

    # Format the transcript
    formatted_text = format_transcript(segments, timestamps=with_timestamps)

    # Handle output
    if output is None:
        output = Path(input_file).with_suffix(".formatted.txt")

    with open(output, "w") as f:
        f.write(formatted_text)

    click.echo(f"Formatted transcript saved to: {output}")


def main():
    """Command line interface for formatting transcripts."""
    cli()


if __name__ == "__main__":
    main()
