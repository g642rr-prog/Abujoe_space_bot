from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# 👇 ضع التوكن اللي خدته من BotFather هنا
TOKEN = "8396425007:AAFz6k-o2iy6Ypo5SfAxcn1ryt2Ga1UwdEA"

def start(update, context):
    update.message.reply_text("""🛁 أهلًا بك في بركس للخدمات!

اختر الخدمة:
1️⃣ سوفت وير وبرامج
2️⃣ أدوات صحية  
3️⃣ استفسارات

ارقم الرقم فقط...""")

def reply(update, context):
    text = update.message.text
    if text == '1':
        update.message.reply_text("💻 برامجنا: محاسبة - مبيعات - إدارة")
    elif text == '2':
        update.message.reply_text("🚰 أدوات صحية: خلاطات - مواسير - حمامات")
    else:
        update.message.reply_text("📞 للاستفسار: 0123456789")

print("🚀 جاري تشغيل البوت...")
updater = Updater(TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, reply))
updater.start_polling()
print("✅ البوت شغال! جربه في تليجرام")
