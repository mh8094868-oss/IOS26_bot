import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# الإعدادات الأساسية
TOKEN = "8637900141:8637900141:AAHbYWiP8NfD1IVs9vyGf1FH8Bjjc_DhKh0"
ADMIN_ID = 8037611619

# القنوات المطلوبة (تأكد أن البوت آدمن فيها)
REQUIRED_CHANNELS = [
    {"username": "@hyperOS31", "id": -1002477232328, "name": "HyperOS 31"},
    {"username": "@notes_xmy", "id": -1003773446325, "name": "Notes XMY"},
]

# الكيبوردات (Keyboards)
main_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("📲 تحميل الثيم", callback_data="download")],
    [InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data="faq")],
    [InlineKeyboardButton("💬 تواصل مع الإدارة", url="https://t.me/Ke_ph1_bot")],
])

back_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="back")]
])

# دالة التحقق من الإشتراك
async def check_subscription(user_id, context: ContextTypes.DEFAULT_TYPE):
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel["id"], user_id=user_id)
            # إذا كانت حالة المستخدم "غادر" أو "مطرود"
            if member.status in ["left", "kicked"]:
                return False
        except Exception as e:
            # في حال وجود خطأ (البوت ليس آدمن أو ID خطأ) نعتبره غير مشترك للأمان
            logging.error(f"Error checking channel {channel['username']}: {e}")
            return False 
    return True

# دالة كيبورد القنوات
def get_channels_keyboard():
    keyboard = []
    for ch in REQUIRED_CHANNELS:
        url = f"https://t.me/{ch['username'].replace('@','')}"
        keyboard.append([InlineKeyboardButton(f"📢 اشترك في {ch['name']}", url=url)])
    keyboard.append([InlineKeyboardButton("✅ تحققت من الاشتراك", callback_data="check_sub")])
    return InlineKeyboardMarkup(keyboard)

# أمر الـ Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    is_subscribed = await check_subscription(user.id, context)
    
    if not is_subscribed:
        channels_list = "\n".join([f"▫️ {ch['name']}" for ch in REQUIRED_CHANNELS])
        text = (
            f"⚠️ عذراً يا بطل، يجب الاشتراك أولاً للمتابعة.\n\n"
            f"قنواتنا:\n{channels_list}\n\n"
            f"✅ بعد الاشتراك، اضغط على زر التحقق بالأسفل."
        )
        await update.message.reply_text(text, reply_markup=get_channels_keyboard())
        return
    
    text = (
        "✨ أهلاً بك في بوت ثيم Ios 26 العربي\n\n"
        "🎨 ثيم زجاجي مائي لهواتف شاومي\n"
        "⚡ يعمل على HyperOS 3\n"
        "⭐ التقييم: 4.9/5\n\n"
        "👇 اختر من الأزرار بالأسفل:"
    )
    await update.message.reply_text(text, reply_markup=main_keyboard)

# معالج الأزرار (Callback Query)
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    data = query.data
    
    await query.answer() # لإيقاف مؤشر التحميل في التليجرام

    if data == "check_sub":
        if await check_subscription(user.id, context):
            await query.answer("✅ تم التحقق بنجاح! نورتنا 🤍", show_alert=True)
            text = "✨ أهلاً بك مجدداً\n\n🎨 ثيم Ios 26 العربي جاهز\n👇 اختر من الأزرار:"
            await query.edit_message_text(text, reply_markup=main_keyboard)
        else:
            await query.answer("❌ لم تشترك في جميع القنوات بعد! 🌚", show_alert=True)

    elif data == "download":
        text = (
            "🚧 الملف قيد التجربة حالياً\n\n"
            "🎨 ثيم Ios 26 العربي تحت الاختبار النهائي\n"
            "📢 سيتم إخبارك فور صدوره في القنوات الرسمية."
        )
        await query.edit_message_text(text, reply_markup=back_keyboard)

    elif data == "faq":
        text = (
            "❓ الأسئلة الشائعة\n\n"
            "1️⃣ هل الثيم مجاني؟\n✅ نعم، متوفر للجميع مجاناً.\n\n"
            "2️⃣ الأنظمة المدعومة؟\n⚡ حصرياً لنظام HyperOS 3.\n\n"
            "3️⃣ الدعم الفني؟\n💬 تواصل معنا عبر: @Ke_ph1_bot"
        )
        await query.edit_message_text(text, reply_markup=back_keyboard)

    elif data == "back":
        text = "✨ القائمة الرئيسية\n\n🎨 ثيم Ios 26 العربي\n👇 اختر من الأزرار:"
        await query.edit_message_text(text, reply_markup=main_keyboard)

# أمر الإحصائيات (للآدمن فقط)
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("✅ نظام الإشتراك الإجباري والخدمات تعمل بشكل مستقر.")

# تشغيل البوت
def main():
    # إعداد السجلات (Logs) لرؤية الأخطاء في التيرمينال
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(callback))
    
    print("🚀 البوت يعمل الآن بنجاح...")
    app.run_polling()

if __name__ == "__main__":
    main()
