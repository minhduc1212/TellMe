import os
import sys

# Ensure UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

os.environ["HF_HOME"] = r"D:\LT\TellMe_TTS\models"
os.environ["HF_HUB_OFFLINE"] = "1"

from vieneu import Vieneu

def main():
    print("🔊 Initializing Vieneu TTS engine...")
    tts = Vieneu()

    # List built-in voices
    voices = tts.list_preset_voices()
    print(f"\n{len(voices)} built-in voices available:")
    for label, voice_id in voices:
        print(f"  - {label} ({voice_id})")

    # Generate sample speech
    sample_text = "Thọc và kéo, bà lão đang nói, đó là cách của Nữ hoàng, cũng giống như chính các vị thần vậy."
    print(f"\n🔊 Generating sample speech with voice 'Phạm Tuyên'...")
    audio = tts.infer(sample_text, voice="Phạm Tuyên")
    
    output_path = "output.wav"
    tts.save(audio, output_path)
    print(f"✅ Audio successfully saved to {output_path}")

if __name__ == "__main__":
    main()