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


if __name__ == "__main__":
    from pathlib import Path

    from tests.segments import TEST_SEGMENTS

    transcript_fpath = Path("/Users/tommylees/Downloads/transcript.txt")
    with open(transcript_fpath, "r") as f:
        transcript = f.read()

    formatted_transcript = format_transcript(TEST_SEGMENTS)
    print(formatted_transcript)
