# Douyin/TikTok Transcriber

A local transcription tool for short videos and audio files.

## Problem

Sometimes I want the transcript of a TikTok/Douyin video, especially Chinese Douyin videos, but many online tools either rely on the platform's built-in captions or require payment for better transcription.

## Goal

Build a tool that accepts an uploaded `.mp3`, `.wav`, or `.mp4` file and generates a transcript without relying on TikTok/Douyin's own transcript.

## Version 1

- Accept a local audio/video file.
- Extract or read the audio.
- Transcribe the speech.
- Save the result as `transcript.txt`.

## Version 2

- Add timestamps.
- Export `.srt` subtitles.

## Version 3

- Add language selection:
  - Chinese
  - English
  - Auto-detect

## Version 4

- Add a simple UI.

## Version 5

- Consider TikTok/Douyin URL support if technically and legally safe.

## Tech Ideas

- Python
- faster-whisper or whisper.cpp
- ffmpeg for extracting audio from video
- optional web UI later