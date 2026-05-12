import telebot
from telebot import types
import os
from flask import Flask, request

API_TOKEN = '8637900141:AAHbYWiP8NfD1IVs9vyGf1FH8Bjjc_DhKh0'
CHANNELS = [
    {"id": -1002477232328, "link": "https://t.me/hyperOS31"},
    {"id": -1003773446325, "link": "https://t.me/notes_xmy"}
]

bot = telebot.TeleBot(API_TOKEN, threaded=False) # threaded=False ضروري لـ Vercel
app = Flask(__name__)

def check_subscription(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel["id"], user_id).status
            if status in ['left', 'kicked']:
                return False
        except:
            return False
    return True

# مسار استقبال رسايل تليجرام (Webhook)
@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# مسار تفعيل الويب هوك (تفتحه مرة وحدة بالمتصفح)
@app.route("/")
def webhook():
    bot.remove_webhook()
    # هنا لازم تحط رابط مشروعك بـ Vercel بعد ما ترفعه
    # bot.set_webhook(url='https://your-project.vercel.app/' + API_TOKEN)
    return "البوت شغال!", 200

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("📲 تحميل الثيم", callback_data="download_theme")
        btn2 = types.InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data="faq")
        btn3 = types.InlineKeyboardButton("💬 تواصل مع الإدارة", url="https://t.me/hyperOS31")
        markup.add(btn1, btn2, btn3)
        welcome_text = "✨ **أهلاً بك في بوت ثيم Ios 26 العربي**..."
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")
    else:
        # كود الاشتراك الإجباري مالتك (نفسه)
        pass

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    # كود معالجة الأزرار مالتك (نفسه)
    if call.data == "download_theme":
        file_path = "po.po" # تأكد الملف مرفوع وية الكود بنفس المجلد
        if os.path.exists(file_path):
            with open(file_path, 'rb') as theme_file:
                bot.send_document(call.message.chat.id, theme_file)
        else:
            bot.answer_callback_query(call.id, "❌ الملف غير موجود", show_alert=True)

# احذف bot.infinity_polling() لأن Flask هو اللي راح يدير الشغل
