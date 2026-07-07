import asyncio
import edge_tts

async def amain():
    communicate = edge_tts.Communicate("Xin chào Đức, đây là giọng đọc miễn phí từ Edge.", "vi-VN-HoaiMyNeural")
    await communicate.save("output.mp3")

asyncio.run(amain())