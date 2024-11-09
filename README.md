# 🎥 YouTube to Text (YTT)

Convert any YouTube video into text transcripts with just one command! Perfect for content creators, researchers, and anyone who needs transcriptions.

Tool built with [uv](https://docs.astral.sh/uv/), [cursor](https://www.cursor.com/) and [OpenAI's Whisper](https://platform.openai.com/docs/guides/speech-recognition).

## ✨ Features

- 🚀 Fast transcription using OpenAI's Whisper model
- 📝 Optional timestamps in transcripts
- 🎵 Audio file preservation (optional)
- 🌟 Support for both regular videos and YouTube Shorts
- 💪 Parallel processing for long videos [TODO]

## 🚀 Quick Start

1. **Install UV** (the fast Python package installer):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone & Install Dependencies**:
```bash
git clone https://github.com/tommylees112/youtube_to_text.git
cd youtube_to_text
uv sync
```

3. **Add to Your Shell** (add to `~/.zshrc` or `~/.bashrc`):
```bash
alias ytt="uv --directory /path/to/youtube_to_text run /path/to/youtube_to_text/ytt.py"
```

4. **Start Transcribing!**
```bash
ytt https://www.youtube.com/watch?v=your_video_id
```

## 🎮 Usage
```bash
# Basic usage
ytt https://www.youtube.com/watch?v=your_video_id

# Save to specific file
ytt https://www.youtube.com/watch?v=your_video_id -o my_transcript.txt

# Save to specific directory
ytt https://www.youtube.com/watch?v=your_video_id -d ~/Documents/transcripts

# Keep the audio file
ytt https://www.youtube.com/watch?v=your_video_id --keep-audio

# Without timestamps
ytt https://www.youtube.com/watch?v=your_video_id --no-timestamps
```

## 🧪 Development
Run the tests:
```python
# fast tests: 
pytest -m "not slow"

# Run integration tests with verbose output
pytest -m integration -v
```

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Feel free to open issues and pull requests.