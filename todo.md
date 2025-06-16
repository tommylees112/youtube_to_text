- [ ] The Real Issue: The YouTube Transcript API has intermittent failures with XML parsing for certain videos. This isn't
   a bug in your code - it's an API reliability issue.

  What we can do:
  1. Add better error handling - catch the XML parsing error and fall back to audio download
  2. Proper URL parsing - use urllib.parse to handle video ID extraction correctly
  3. Support direct video IDs - allow passing just Cybnip2Kyw0 as input
  4. Retry logic - attempt transcript API multiple times before falling back

  The YouTube Transcript API sometimes returns malformed XML, causing the parsing error. Your fallback to audio
  download + Whisper is the right approach when this happens.