from src.format_transcript import format_timestamp, format_transcript
from tests.segments import TEST_SEGMENTS


def test_format_timestamp():
    test_cases = [
        (0, "00:00:00"),
        (61, "00:01:01"),
        (3600, "01:00:00"),
        (3661, "01:01:01"),
        (7323, "02:02:03"),
    ]

    for seconds, expected in test_cases:
        assert format_timestamp(seconds) == expected


def test_format_transcript_with_timestamps():
    formatted = format_transcript(TEST_SEGMENTS, timestamps=True)
    expected = "[00:00:00 -> 00:00:05] Japan invades Manchuria in 1931, Hitler invades Poland in 1939, and in retrospect, we think of\n[00:00:05 -> 00:00:09] them as part of the same great global conflict, whereas they were separated by eight years.\n"
    assert formatted == expected


def test_format_transcript_without_timestamps():
    formatted = format_transcript(TEST_SEGMENTS, timestamps=False)
    expected = "Japan invades Manchuria in 1931, Hitler invades Poland in 1939, and in retrospect, we think of them as part of the same great global conflict, whereas they were separated by eight years.\n"
    assert formatted == expected
