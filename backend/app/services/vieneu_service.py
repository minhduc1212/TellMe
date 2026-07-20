import os
import sys
import uuid
import wave
import contextlib
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional

# Set HF path and offline mode
os.environ["HF_HOME"] = r"D:\LT\TellMe_TTS\models"
os.environ["HF_HUB_OFFLINE"] = "1"

try:
    from vieneu import Vieneu
    VIENEU_AVAILABLE = True
except Exception as e:
    print(f"Warning: Failed to import vieneu: {e}")
    VIENEU_AVAILABLE = False

class VieneuService:
    _instance = None
    _model = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = VieneuService()
        return cls._instance

    def __init__(self):
        self._model = None

    def _ensure_model_loaded(self):
        if self._model is None:
            if not VIENEU_AVAILABLE:
                raise RuntimeError("Vieneu package is not available.")
            print("🔊 Lazy loading Vieneu model...")
            self._model = Vieneu()

    def list_preset_voices(self) -> List[Dict[str, Any]]:
        try:
            self._ensure_model_loaded()
            raw_voices = self._model.list_preset_voices()
            voices = []
            for label, voice_id in raw_voices:
                voices.append({
                    "id": f"vieneu_{voice_id}",
                    "name": voice_id,
                    "voice_id": voice_id,
                    "engine": "vieneu",
                    "lang": "vi-VN",
                    "gender": "Female" if "Nữ" in label else "Male",
                    "supports_cloning": True,
                    "description": label
                })
            return voices
        except Exception as e:
            print(f"Error listing Vieneu voices: {e}")
            # Fallback preset list
            return [
                {"id": "vieneu_pham_tuyen", "name": "Phạm Tuyên", "voice_id": "Phạm Tuyên", "engine": "vieneu", "lang": "vi-VN", "gender": "Male", "accent": "Bắc", "style": "Tự nhiên", "supports_cloning": True, "description": "Phạm Tuyên — Nam · Bắc · Phong cách tự nhiên"},
                {"id": "vieneu_truc_ly", "name": "Trúc Ly", "voice_id": "Trúc Ly", "engine": "vieneu", "lang": "vi-VN", "gender": "Female", "accent": "Bắc", "style": "Tự nhiên", "supports_cloning": True, "description": "Trúc Ly — Nữ · Bắc · Phong cách tự nhiên"},
                {"id": "vieneu_thai_son", "name": "Thái Sơn", "voice_id": "Thái Sơn", "engine": "vieneu", "lang": "vi-VN", "gender": "Male", "accent": "Nam", "style": "Kể chuyện", "supports_cloning": True, "description": "Thái Sơn — Nam · Nam · Phong cách kể chuyện"},
                {"id": "vieneu_xuan_vinh", "name": "Xuân Vĩnh", "voice_id": "Xuân Vĩnh", "engine": "vieneu", "lang": "vi-VN", "gender": "Male", "accent": "Bắc", "style": "Tự nhiên", "supports_cloning": True, "description": "Xuân Vĩnh — Nam · Bắc · Phong cách tự nhiên"},
                {"id": "vieneu_thanh_binh", "name": "Thanh Bình", "voice_id": "Thanh Bình", "engine": "vieneu", "lang": "vi-VN", "gender": "Male", "accent": "Bắc", "style": "Kể chuyện", "supports_cloning": True, "description": "Thanh Bình — Nam · Bắc · Phong cách kể chuyện"},
                {"id": "vieneu_minh_duc", "name": "Minh Đức", "voice_id": "Minh Đức", "engine": "vieneu", "lang": "vi-VN", "gender": "Male", "accent": "Bắc", "style": "Tin tức", "supports_cloning": True, "description": "Minh Đức — Nam · Bắc · Phong cách tin tức"},
                {"id": "vieneu_ngoc_linh", "name": "Ngọc Linh", "voice_id": "Ngọc Linh", "engine": "vieneu", "lang": "vi-VN", "gender": "Female", "accent": "Bắc", "style": "Kể chuyện", "supports_cloning": True, "description": "Ngọc Linh — Nữ · Bắc · Phong cách kể chuyện"},
                {"id": "vieneu_doan_trang", "name": "Đoan Trang", "voice_id": "Đoan Trang", "engine": "vieneu", "lang": "vi-VN", "gender": "Female", "accent": "Bắc", "style": "Tự nhiên", "supports_cloning": True, "description": "Đoan Trang — Nữ · Bắc · Phong cách tự nhiên"},
                {"id": "vieneu_mai_anh", "name": "Mai Anh", "voice_id": "Mai Anh", "engine": "vieneu", "lang": "vi-VN", "gender": "Female", "accent": "Bắc", "style": "Tin tức", "supports_cloning": True, "description": "Mai Anh — Nữ · Bắc · Phong cách tin tức"},
                {"id": "vieneu_thuc_doan", "name": "Thục Đoan", "voice_id": "Thục Đoan", "engine": "vieneu", "lang": "vi-VN", "gender": "Female", "accent": "Nam", "style": "Kể chuyện", "supports_cloning": True, "description": "Thục Đoan — Nữ · Nam · Phong cách kể chuyện"}
            ]

    def generate_speech(
        self,
        text: str,
        voice_id: Optional[str] = "Phạm Tuyên",
        ref_audio_path: Optional[str] = None,
        output_dir: str = "backend/static/audio",
        speed: float = 1.0,
        temperature: float = 0.8
    ) -> Dict[str, Any]:
        self._ensure_model_loaded()

        os.makedirs(output_dir, exist_ok=True)
        file_id = f"vieneu_{uuid.uuid4().hex[:10]}"
        output_path = os.path.join(output_dir, f"{file_id}.wav")

        # Strip prefix if passed
        clean_voice_id = voice_id.replace("vieneu_", "") if voice_id else "Phạm Tuyên"
        
        # Match voice ID with available preset voices in Vieneu
        preset_voices = self._model.list_preset_voices()
        voice_param = "Phạm Tuyên"
        
        matched = False
        for label, vid in preset_voices:
            if clean_voice_id in [label, vid] or clean_voice_id == vid or clean_voice_id == label or vid in clean_voice_id:
                voice_param = vid
                matched = True
                break

        if not matched and preset_voices:
            voice_param = preset_voices[0][1]

        print(f"🔊 Vieneu generating speech: voice='{voice_param}', ref_audio='{ref_audio_path}'")
        
        if ref_audio_path and os.path.exists(ref_audio_path):
            audio = self._model.infer(text, ref_audio=ref_audio_path, denoise=True, temperature=temperature)
        else:
            audio = self._model.infer(text, voice=voice_param, temperature=temperature)

        self._model.save(audio, output_path)

        # Get audio duration
        duration = self._get_wav_duration(output_path)

        # Generate estimated word timestamps for UI word-highlighting
        words_timestamps = self._estimate_word_timestamps(text, duration)

        return {
            "id": file_id,
            "filename": f"{file_id}.wav",
            "filepath": output_path,
            "url": f"/static/audio/{file_id}.wav",
            "duration": round(duration, 2),
            "engine": "vieneu",
            "voice": voice_param,
            "text": text,
            "words": words_timestamps
        }

    def _get_wav_duration(self, filepath: str) -> float:
        try:
            with contextlib.closing(wave.open(filepath, 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                return duration
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
