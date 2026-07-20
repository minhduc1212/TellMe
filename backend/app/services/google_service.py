import os
import uuid
from typing import Dict, Any, List
from gtts import gTTS

class GoogleTTSService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = GoogleTTSService()
        return cls._instance

    def list_voices(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "google_vi",
                "name": "Google Translate (Tiếng Việt)",
                "voice_id": "vi",
                "engine": "google",
                "lang": "vi-VN",
                "gender": "Female",
                "supports_cloning": False,
                "description": "Giọng đọc Google Translate tiêu chuẩn"
            },
            {
                "id": "google_en",
                "name": "Google Translate (English)",
                "voice_id": "en",
                "engine": "google",
                "lang": "en-US",
                "gender": "Female",
                "supports_cloning": False,
                "description": "Standard English Google voice"
            }
        ]

    def generate_speech(
        self,
        text: str,
        lang: str = "vi",
        output_dir: str = "backend/static/audio",
        slow: bool = False
    ) -> Dict[str, Any]:
        os.makedirs(output_dir, exist_ok=True)
        file_id = f"google_{uuid.uuid4().hex[:10]}"
        output_path = os.path.join(output_dir, f"{file_id}.mp3")

        clean_lang = lang.replace("google_", "")
        if clean_lang not in ["vi", "en", "ja", "fr", "zh-CN"]:
            clean_lang = "vi"

        tts = gTTS(text=text, lang=clean_lang, slow=slow)
        tts.save(output_path)

        duration = self._estimate_duration(output_path, text)
        words_timestamps = self._estimate_word_timestamps(text, duration)

        return {
            "id": file_id,
            "filename": f"{file_id}.mp3",
            "filepath": output_path,
            "url": f"/static/audio/{file_id}.mp3",
            "duration": round(duration, 2),
            "engine": "google",
            "voice": clean_lang,
            "text": text,
            "words": words_timestamps
        }

    def _estimate_duration(self, filepath: str, text: str) -> float:
        try:
            size = os.path.getsize(filepath)
            # gTTS mp3 bit rate is roughly 32 kbps -> 4000 bytes/sec
            return max(1.5, size / 4000.0)
        except Exception:
            # Approx 4 words per second
            words = text.split()
            return max(1.5, len(words) / 4.0)

    def _estimate_word_timestamps(self, text: str, duration: float) -> List[Dict[str, Any]]:
        words = text.strip().split()
        if not words:
            return []
        
        total_chars = sum(len(w) for w in words)
        if total_chars == 0:
            return []

        current_time = 0.0
        word_data = []

        for w in words:
            word_duration = (len(w) / total_chars) * duration
            end_time = current_time + word_duration
            word_data.append({
                "word": w,
                "start": round(current_time, 2),
                "end": round(end_time, 2)
            })
            current_time = end_time

        return word_data
