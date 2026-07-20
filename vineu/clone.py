import os
import sys
from pathlib import Path

# Ensure UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

os.environ["HF_HOME"] = r"D:\LT\TellMe_TTS\models"
os.environ["HF_HUB_OFFLINE"] = "1"

from vieneu import Vieneu

def clone_voice(ref_audio_path: str, text: str, output_path: str = "cloned_output.wav"):
    """
    Zero-shot voice cloning using Vieneu TTS.
    
    :param ref_audio_path: Path to the reference audio clip (.wav or .mp3)
    :param text: Vietnamese text to synthesize with cloned voice
    :param output_path: Path to save generated audio
    """
    if not os.path.exists(ref_audio_path):
        print(f"❌ Error: Reference audio file '{ref_audio_path}' not found.")
        return False

    print(f"🔊 Initializing Vieneu TTS for voice cloning...")
    tts = Vieneu()

    print(f"🎙️ Cloning voice from reference audio: '{ref_audio_path}'...")
    print(f"💬 Target text: \"{text}\"")
    
    audio = tts.infer(text, ref_audio=ref_audio_path, denoise=True)
    tts.save(audio, output_path)
    print(f"✅ Voice cloned successfully! Saved to '{output_path}'")
    return True

if __name__ == "__main__":
    ref_clip = "output.wav"  # Use output.wav as reference if available
    sample_target = "Chào mừng bạn đến với hệ thống chuyển đổi văn bản thành giọng nói Vieneu TTS."
    
    if len(sys.argv) > 1:
        ref_clip = sys.argv[1]
    if len(sys.argv) > 2:
        sample_target = sys.argv[2]
        
    clone_voice(ref_clip, sample_target)
