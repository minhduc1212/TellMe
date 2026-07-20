import asyncio
import sys
import edge_tts

# Ensure UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

async def generate_edge_tts(
    text: str,
    voice: str = "vi-VN-HoaiMyNeural",
    output_file: str = "output.mp3",
    rate: str = "+0%",
    pitch: str = "+0Hz",
    volume: str = "+0%"
):
    """
    Generate audio using Microsoft Edge TTS neural voices.
    """
    print(f"🔊 Generating Edge TTS audio with voice '{voice}'...")
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
        volume=volume
    )
    await communicate.save(output_file)
    print(f"✅ Edge TTS audio saved to '{output_file}'")

def main():
    text = "Xin chào Đức, đây là giọng đọc miễn phí từ Microsoft Edge Neural TTS."
    asyncio.run(generate_edge_tts(text, voice="vi-VN-HoaiMyNeural", output_file="output.mp3"))

if __name__ == "__main__":
    main()