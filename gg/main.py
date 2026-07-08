from gtts import gTTS

def main():
    # Văn bản cần chuyển đổi
    text = "Xin chào, đây là giọng đọc chuẩn của Google hoàn toàn miễn phí."
    
    # Tạo đối tượng TTS
    # lang='vi': Chọn ngôn ngữ Tiếng Việt
    # slow=False: Đọc ở tốc độ bình thường (đặt True nếu muốn đọc chậm từng chữ)
    tts = gTTS(text=text, lang='vi', slow=False)
    
    # Lưu file âm thanh
    file_name = "google_voice.mp3"
    tts.save(file_name)
    
    print(f"Đã xuất file âm thanh thành công: {file_name}")

if __name__ == "__main__":
    main()