import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

TOKEN = "8637900141:AAEAH85RdTUVhz488aALryiW1Wxcob6c3uY"
ADMIN_ID = 8037611619

REQUIRED_CHANNELS = [
    {"username": "@hyperOS31", "id": -1002477232328, "name": "HyperOS 31"},
    {"username": "@notes_xmy", "id": -1003773446325, "name": "Notes XMY"},
]

main_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("📲 تحميل الثيم", callback_data="download")],
    [InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data="faq")],
    [InlineKeyboardButton("💬 تواصل مع الإدارة", url="https://t.me/Ke_ph1_bot")],
])

back_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="back")]
])

async def check_subscription(user_id, context):
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel["id"], user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            continue
    return True

def get_channels_keyboard():
    keyboard = []
    for ch in REQUIRED_CHANNELS:
        keyboard.append([InlineKeyboardButton(f"📢 اشترك في {ch['name']}", url=f"https://t.me/{ch['username'].replace('@','')}")])
    keyboard.append([InlineKeyboardButton("✅ تحققت من الاشتراك", callback_data="check_sub")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context):
    user = update.effective_user
    is_subscribed = await check_subscription(user.id, context)
    
    if not is_subscribed:
        channels_list = "\n".join([f"▫️ {ch['name']}" for ch in REQUIRED_CHANNELS])
        text = f"⚠️ عذراً، يجب الاشتراك أولاً\n\nللمتابعة، اشترك في القنوات:\n\n{channels_list}\n\n✅ بعد الاشتراك اضغط: تحققت من الاشتراك"
        await update.message.reply_text(text, reply_markup=get_channels_keyboard())
        return
    
    text = "✨ أهلاً بك في بوت ثيم Ios 26 العربي\n\n🎨 ثيم زجاجي مائي لهواتف شاومي\n⚡ يعمل على HyperOS 3\n⭐ التقييم: 4.9/5\n\n👇 اختر من الأزرار:"
    await update.message.reply_text(text, reply_markup=main_keyboard)

async def callback(update: Update, context):
    query = update.callback_query
    await query.answer()
    data = query.data
    user = update.effective_user
    
    if data == "check_sub":
        is_subscribed = await check_subscription(user.id, context)
        if not is_subscribed:
            await query.answer("❌ لم تشترك بعد! اشترك وحاول", show_alert=True)
            text = "⚠️ لم تكمل الاشتراك\n\nاشترك ثم اضغط الزر"
            await query.edit_message_text(text, reply_markup=get_channels_keyboard())
        else:
            await query.answer("✅ تم التحقق! أهلاً بك 🤍", show_alert=True)
            text = "✅ تم التحقق بنجاح\n\n🎨 ثيم Ios 26 العربي\n⭐ التقييم: 4.9/5\n\n👇 اختر من الأزرار:"
            await query.edit_message_text(text, reply_markup=main_keyboard)
    
    elif data == "download":
        text = "🚧 الملف قيد التجربة\n\n🎨 ثيم Ios 26 العربي تحت الاختبار\n\n📢 سيتم إخبارك فور صدوره:\n@hyperOS31\n@notes_xmy\n\n💬 للاستفسار: @Ke_ph1_bot"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 HyperOS 31", url="https://t.me/hyperOS31")],
            [InlineKeyboardButton("📢 Notes XMY", url="https://t.me/notes_xmy")],
            [InlineKeyboardButton("💬 تواصل", url="https://t.me/Ke_ph1_bot")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back")],
        ])
        await query.edit_message_text(text, reply_markup=keyboard)
    
    elif data == "faq":
        text = "❓ الأسئلة الشائعة\n\n1- هل الثيم مجاني؟\n✅ نعم 100%\n\n2- الأنظمة المدعومة؟\n⚡ HyperOS 3 فقط\n\n3- موعد الإصدار؟\n📅 قريباً\n\n4- الدعم الفني؟\n💬 @Ke_ph1_bot"
        await query.edit_message_text(text, reply_markup=back_keyboard)
    
    elif data == "back":
        text = "✨ القائمة الرئيسية\n\n🎨 ثيم Ios 26 العربي\n⭐ 4.9/5\n\n👇 اختر:"
        await query.edit_message_text(text, reply_markup=main_keyboard)

async def stats(update: Update, context):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("✅ البوت شغال")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(callback))
    print("✅ بوت Ios 26 شغال...")
    app.run_polling()

if __name__ == "__main__":
    main()