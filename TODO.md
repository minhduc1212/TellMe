# TellMe TTS — Text-to-Speech & Voice Cloning Web Application

## Overview
TellMe TTS is a web application for high-quality Vietnamese text-to-speech synthesis, zero-shot voice cloning, and multi-provider audio generation.

## Implemented Tech Stack & Architecture
- **Backend**: Python FastAPI (`backend/app/main.py`), Uvicorn server, REST API.
  - **Vieneu Engine**: High-fidelity 48kHz Vietnamese neural voices + zero-shot voice cloning.
  - **Edge TTS Engine**: Microsoft Edge Neural multi-language voices (`vi-VN-HoaiMyNeural`, `vi-VN-NamMinhNeural`, `en-US`, `ja-JP`, `fr-FR`) with speed and pitch control.
  - **Google TTS Engine**: gTTS fallback for quick online synthesis.
- **Frontend**: Vue 3 (Composition API `<script setup>`), Vite, Vanilla CSS design tokens following `DESIGN.md`.
  - Electric Indigo (`#4f46e5`) primary action fill.
  - Cyan Signal (`#06b6d4`) live audio indicator & real-time spoken word highlight.
  - Canvas White (`#ffffff`) editor workspace.
  - Sticky bottom audio player with circular play/pause button, animated SVG waveform, and MP3/WAV download button.
  - Audio history drawer with playback and management.

## How to Run

### 1. Start Backend Server
```bash
.venv\Scripts\python.exe backend/run.py
# Server runs on http://127.0.0.1:8000
```

### 2. Start Frontend Dev Server
```bash
cd frontend
npm run dev
# Frontend runs on http://localhost:5173
```


