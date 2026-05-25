# Media Transcriber

A Streamlit web app for transcribing short audio and video files using `faster-whisper`.
The app accepts uploaded media files, runs speech-to-text transcription, and outputs a downloadable transcript with optional timestamps and line numbers.\
Web version: https://media-transcriber.streamlit.app
## Problem

Sometimes I want the transcript of a TikTok/Douyin videos, but many online tools either rely on the platform's built-in captions or require payment for better transcription.
This project is an attempt to build my own transcription tool that works from an uploaded local media file instead of relying on TikTok/Douyin’s built-in captions.

## Features

- Upload local audio/video files
- Preview uploaded audio/video inside the app
- Transcribe speech using `faster-whisper`
- Transcription options such as language, timestamps
- Download transcript as `.txt`
- Cached Whisper model loading for faster repeated transcriptions
- Temporary file handling for uploads

## Tech stack
- Python
- Streamlit
- faster-whisper
- Git/Github

## Current Version

### Version 7.5

- improved transcription accuracy by 
  - switching whisper model from "tiny" to "base"
  - additional transcribe settings "vad_filter=True, condition_on_previous_text=False"
  - made vad_filter and condition_on_previous settings optional, as enabling either/both/none could result in different results depending on the media's audio 

## Development progress

### Version 1
- streamlit
- fake transcripter that haven't implemented faster-whisper model
- Accept a local audio/video file.
- Extract or read the audio.
- Transcribe the speech.
- Save the result as a fake `transcript.txt`.

### Version 2

- implemented simple timestamps function.

### Version 3

- Add language selection:
  - Chinese
  - English
  - Auto-detect

### Version 4

- implemented the faster-whisper model, transcripts are no longer fake.

### Version 5

- implemented the faster-whisper model to cache (so streamlit wouldn't load it again every time i transcribe)

### Version 6

- made timestamp and line_number optionals
- launched the app on streamlit's community cloud

## Known Issues / Limitations

- Due to the web version using streamlit's community cloud, after a period of inactivity when opening the app again it will require a couple minutes to "wake the website up"
- Transcription quality vary between the local version and the deployed Streamlit Community Cloud version
  - The local version runs on my laptop.
  - The deployed version runs on Streamlit Cloud’s server CPU and environment.
  - This can cause differences in speed, audio decoding, model behaviour, and final transcript quality.
- Korean or noisy audio/video files likely to produce lower-quality transcripts on the hosted demo compared to local testing.
  - This is more noticeable with music, background noise, unclear vocals, or short speech fragments.
  - Version 7 improved this by switching from `tiny` model to `base` model and adding hallucination-reduction settings.
- The hosted app is a prototype, not a production transcription service.
  - Long files may be slow.
  - Large files may fail depending on cloud resource limits.
- TikTok/Douyin URL input is not currently supported.
  - The app currently works with local files only.

## Future versions
- Add `.srt` and `.vtt` subtitle export
- Improve UI and styling
- Add support for transcript history
  - which would lead to account creation stuff
- Rebuild the prototype into a fuller web app using:
  - React
  - Tailwind CSS
  - Node.js/Express or FastAPI
  - SQL database
- Run faster-whisper transcription on the user’s device using browser-based models such as Transformers.js
- Consider TikTok/Douyin URL support

## How to Run Locally

Clone the repository:

```bash
git clone https://github.com/EtreanSea/media-transcriber.git
cd media-transcriber