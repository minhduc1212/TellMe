import os

os.environ["HF_HOME"] = r"D:\LT\TellMe_TTS\models"
os.environ["HF_HUB_OFFLINE"] = "1"
from vieneu import Vieneu

# Default = v3 Turbo (48 kHz). GPU → PyTorch (auto-detected).
tts = Vieneu()

# 1. Built-in voice by name — no reference clip needed
print("🔊 Generating speech...")
audio = tts.infer("[cười] Trời ơi, cái giọng nó tự nhiên mà nó mượt mà dã man, nghe không khác gì người thật luôn. Giờ thì tha hồ mà quẩy content với cả kho giọng nói đa dạng, đủ mọi sắc thái biểu cảm. Mọi người bật loa lên rồi cùng trải nghiệm thử với mình nhé!", voice="Phạm Tuyên")
tts.save(audio, "output.wav")
print("Saved to output.wav")

# List the built-in voices
voices = tts.list_preset_voices()
print(f"\n{len(voices)} built-in voices available:")
for label, voice_id in voices:
    print(f"  - {label} ({voice_id})")