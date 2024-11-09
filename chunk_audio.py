import concurrent.futures
import os
from pathlib import Path
from typing import Literal

import whisper
from loguru import logger
from pydub import AudioSegment


def chunk_audio(audio_path: Path, chunk_duration: int = 300) -> list[Path]:
    """Split audio file into chunks of specified duration (in seconds)."""
    audio = AudioSegment.from_mp3(str(audio_path))
    chunks = []

    for i in range(0, len(audio), chunk_duration * 1000):
        chunk = audio[i : i + chunk_duration * 1000]
        chunk_path = audio_path.parent / f"chunk_{i//1000}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)

    return chunks


def transcribe_chunk(
    chunk_path: Path, model_str: Literal["base", "turbo"] = "turbo"
) -> dict:
    """Transcribe a single audio chunk."""
    model = whisper.load_model(model_str)
    try:
        result = model.transcribe(
            str(chunk_path),
            word_timestamps=True,
        )
        # Clean up chunk file
        os.remove(chunk_path)
        return result["segments"]
    except Exception as e:
        logger.error(f"Chunk transcription failed: {e}")
        raise


def transcribe_chunks(
    audio_path: Path, chunk_duration: int = 300, max_workers: int = 4
):
    logger.info("Splitting audio_path into chunks...")
    chunks = chunk_audio(audio_path=audio_path, chunk_duration=chunk_duration)
    logger.info(f"Split into {len(chunks)} chunks")

    # Process chunks in parallel
    logger.info("Starting parallel transcription...")
    all_segments = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_chunk = {
            executor.submit(transcribe_chunk, chunk): i
            for i, chunk in enumerate(chunks)
        }

        for future in concurrent.futures.as_completed(future_to_chunk):
            chunk_idx = future_to_chunk[future]
            try:
                segments = future.result()
                # Adjust timestamps based on chunk position
                for segment in segments:
                    segment["start"] += (
                        chunk_idx * chunk_duration
                    )  # Add offset based on chunk position
                    segment["end"] += chunk_idx * chunk_duration
                all_segments.extend(segments)
            except Exception as e:
                logger.error(f"Chunk {chunk_idx} failed: {e}")

    # Sort segments by start time
    all_segments.sort(key=lambda x: x["start"])
    return all_segments


if __name__ == "__main__":
    from pathlib import Path

    from format_transcript import format_transcript

    audio_file = Path(
        "/Users/tommylees/Downloads/could_the_war_in_ukraine_escalate_into_a_world_war.mp3"
    )
    assert audio_file.exists(), logger.error(f"Audio file not found: {audio_file}")

    segments = transcribe_chunks(audio_file, chunk_duration=300)
    print(segments)

    transcript = format_transcript(segments)
    print(transcript)

    with open("transcript_chunked.txt", "w") as f:
        f.write(transcript)

    raise AssertionError
