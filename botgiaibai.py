import telebot
import pytesseract
from PIL import Image
import os

# Token từ BotFather
TOKEN = '7423151024:AAGlugINd8VzRzHQata1zZAPVMAApQuPfxc'
bot = telebot.TeleBot(TOKEN)

# Xử lý khi người dùng gửi ảnh
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Lấy ảnh từ tin nhắn của người dùng
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Lưu ảnh vào thư mục tạm thời
        img_path = 'temp_image.jpg'
        with open(img_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Nhận diện văn bản từ ảnh sử dụng Tesseract OCR
        text = pytesseract.image_to_string(Image.open(img_path), lang='eng')
        bot.reply_to(message, f'Văn bản nhận diện được: {text}')
        
        # Hàm giả định để giải bài tập
        result = solve_task(text)
        bot.send_message(message.chat.id, result)

        # Xóa ảnh sau khi xử lý
        os.remove(img_path)
    except Exception as e:
        bot.reply_to(message, 'Có lỗi xảy ra khi xử lý ảnh. Vui lòng thử lại sau.')
        print(e)

# Hàm giả lập giải bài tập từ văn bản nhận diện
def solve_task(text):
    # Ví dụ: giải các phép toán đơn giản
    if "2 + 2" in text:
        return "Kết quả: 4"
    elif "3 * 3" in text:
        return "Kết quả: 9"
    else:
        return "Không thể giải bài tập này. Vui lòng gửi một bài khác."

# Xử lý khi người dùng gửi lệnh "/start"
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Chào bạn! Hãy gửi cho tôi một ảnh bài tập và tôi sẽ giải giúp bạn.")

# Chạy bot
bot.polling()
