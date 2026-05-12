import telebot
from telebot import types
import os

API_TOKEN = '8637900141:AAHbYWiP8NfD1IVs9vyGf1FH8Bjjc_DhKh0'
CHANNELS = [
    {"id": -1002477232328, "link": "https://t.me/hyperOS31"},
    {"id": -1003773446325, "link": "https://t.me/notes_xmy"}
]

bot = telebot.TeleBot(API_TOKEN)

def check_subscription(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel["id"], user_id).status
            if status in ['left', 'kicked']:
                return False
        except:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    if check_subscription(user_id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        # هنا غيرنا الزر من رابط إلى callback_data حتى البوت يدز الملف
        btn1 = types.InlineKeyboardButton("📲 تحميل الثيم", callback_data="download_theme")
        btn2 = types.InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data="faq")
        btn3 = types.InlineKeyboardButton("💬 تواصل مع الإدارة", url="https://t.me/hyperOS31")
        markup.add(btn1, btn2, btn3)

        welcome_text = (
            "✨ **أهلاً بك في بوت ثيم Ios 26 العربي**\n\n"
            "🎨 **ثيم زجاجي مائي لهواتف شاومي**\n"
            "⚡ **يعمل على HyperOS 3**\n"
            "⭐ **التقييم: 4.9/5**\n\n"
            "👇 **اختر من الأزرار:**"
        )
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")
    
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i, channel in enumerate(CHANNELS, 1):
            markup.add(types.InlineKeyboardButton(f"قناة الاشتراك {i} ✅", url=channel["link"]))
        markup.add(types.InlineKeyboardButton("تحقق من الاشتراك 🔄", callback_data="check"))
        
        bot.send_message(message.chat.id, 
                         "⚠️ **عذراً عزيزي، عليك الاشتراك في قنوات البوت أولاً!**\n\n"
                         "اشترك بالقنوات جوه واضغط على زر التحقق 👇", 
                         reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "check":
        if check_subscription(call.from_user.id):
            bot.answer_callback_query(call.id, "✅ تم التحقق بنجاح!")
            bot.delete_message(call.message.chat.id, call.message.message_id)
            start(call.message)
        else:
            bot.answer_callback_query(call.id, "❌ لسه ما اشتركت بكل القنوات!", show_alert=True)
            
    elif call.data == "download_theme":
        # التحقق من وجود الملف قبل الإرسال
        file_path = "po.po"
        if os.path.exists(file_path):
            bot.answer_callback_query(call.id, "جاري إرسال الثيم... ⏳")
            with open(file_path, 'rb') as theme_file:
                bot.send_document(call.message.chat.id, theme_file, caption="✅ تفضل عزيزي، هذا ملف الثيم الخاص بك.")
        else:
            bot.answer_callback_query(call.id, "❌ الملف غير موجود حالياً، تواصل مع المطور.", show_alert=True)

    elif call.data == "faq":
        bot.answer_callback_query(call.id, "الأسئلة الشائعة ستتوفر قريباً!")

print("البوت شغال حالياً...")
bot.infinity_polling()
