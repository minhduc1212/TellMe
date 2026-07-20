import sys
from gtts import gTTS

# Ensure UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def generate_gtts(text: str, lang: str = "vi", slow: bool = False, output_file: str = "google_voice.mp3"):
    """
    Generate audio using Google Translate TTS (gTTS).
    """
    print(f"🔊 Generating Google TTS audio (lang='{lang}')...")
    tts = gTTS(text=text, lang=lang, slow=slow)
    tts.save(output_file)
    print(f"✅ Google TTS audio saved to '{output_file}'")

def main():
    text = "Xin chào, đây là giọng đọc chuẩn của Google hoàn toàn miễn phí."
    generate_gtts(text, lang="vi", output_file="google_voice.mp3")

if __name__ == "__main__":
    main()