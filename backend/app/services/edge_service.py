import os
import uuid
import asyncio
import edge_tts
from typing import Dict, Any, List, Optional
try:
    from mutagen.mp3 import MP3
    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False

class EdgeTTSService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = EdgeTTSService()
        return cls._instance

    def list_voices(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "edge_vi-VN-HoaiMyNeural",
                "name": "Hoài My (Edge Neural)",
                "voice_id": "vi-VN-HoaiMyNeural",
                "engine": "edge",
                "lang": "vi-VN",
                "gender": "Female",
                "supports_cloning": False,
                "description": "Giọng nữ chuẩn Hà Nội, mượt mà và tự nhiên"
            },
            {
                "id": "edge_vi-VN-NamMinhNeural",
                "name": "Nam Minh (Edge Neural)",
                "voice_id": "vi-VN-NamMinhNeural",
                "engine": "edge",
                "lang": "vi-VN",
                "gender": "Male",
                "supports_cloning": False,
                "description": "Giọng nam chuẩn Hà Nội, chuyên nghiệp và rõ ràng"
            },
            {
                "id": "edge_en-US-JennyNeural",
                "name": "Jenny (English US)",
                "voice_id": "en-US-JennyNeural",
                "engine": "edge",
                "lang": "en-US",
                "gender": "Female",
                "supports_cloning": False,
                "description": "American English female voice, energetic & clear"
            },
            {
                "id": "edge_en-US-GuyNeural",
                "name": "Guy (English US)",
                "voice_id": "en-US-GuyNeural",
                "engine": "edge",
                "lang": "en-US",
                "gender": "Male",
                "supports_cloning": False,
                "description": "American English male voice, deep & natural"
            },
            {
                "id": "edge_ja-JP-NanamiNeural",
                "name": "Nanami (Japanese)",
                "voice_id": "ja-JP-NanamiNeural",
                "engine": "edge",
                "lang": "ja-JP",
                "gender": "Female",
                "supports_cloning": False,
                "description": "Japanese female neural voice"
            },
            {
                "id": "edge_fr-FR-DeniseNeural",
                "name": "Denise (French)",
                "voice_id": "fr-FR-DeniseNeural",
                "engine": "edge",
                "lang": "fr-FR",
                "gender": "Female",
                "supports_cloning": False,
                "description": "French female neural voice"
            }
        ]

    async def generate_speech(
        self,
        text: str,
        voice_id: str = "vi-VN-HoaiMyNeural",
        output_dir: str = "backend/static/audio",
        speed: float = 1.0,
        pitch: float = 0.0,
        volume: float = 0.0
    ) -> Dict[str, Any]:
        os.makedirs(output_dir, exist_ok=True)
        file_id = f"edge_{uuid.uuid4().hex[:10]}"
        output_path = os.path.join(output_dir, f"{file_id}.mp3")

        clean_voice_id = voice_id.replace("edge_", "")

        # Format rate string: speed 1.0 -> "+0%", speed 1.25 -> "+25%", speed 0.8 -> "-20%"
        rate_pct = int((speed - 1.0) * 100)
        rate_str = f"{'+' if rate_pct >= 0 else ''}{rate_pct}%"

        # Format pitch string: pitch 0.0 -> "+0Hz", pitch 10.0 -> "+10Hz"
        pitch_int = int(pitch)
        pitch_str = f"{'+' if pitch_int >= 0 else ''}{pitch_int}Hz"

        # Format volume string
        vol_int = int(volume)
        vol_str = f"{'+' if vol_int >= 0 else ''}{vol_int}%"

        communicate = edge_tts.Communicate(
            text=text,
            voice=clean_voice_id,
            rate=rate_str,
            pitch=pitch_str,
            volume=vol_str
        )

        await communicate.save(output_path)

        duration = self._get_audio_duration(output_path)
        words_timestamps = self._estimate_word_timestamps(text, duration)

        return {
            "id": file_id,
            "filename": f"{file_id}.mp3",
            "filepath": output_path,
            "url": f"/static/audio/{file_id}.mp3",
            "duration": round(duration, 2),
            "engine": "edge",
            "voice": clean_voice_id,
            "text": text,
            "words": words_timestamps
        }

    def _get_audio_duration(self, filepath: str) -> float:
        if HAS_MUTAGEN:
            try:
                audio = MP3(filepath)
                return audio.info.length
            except Exception:
                pass
        try:
            size = os.path.getsize(filepath)
            return max(1.0, size / 16000.0)
        except Exception:
            return 3.0

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
