import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler, filters
from openai import OpenAI

# إعداد اللوج
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# قراءة المفاتيح من المتغيرات السرّية (Secrets)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# تهيئة عميل OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# ✅ رسالة الترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    welcome_message = (
        f"أهلاً بيك يا {user} 😄\n"
        f"في أبو جو للتطوير الفضائي والسوفت وير والأدوات الصحية 🚀🛠️\n"
        f"قولي أخدمك إزاي يا عم الناس؟ 😃"
    )
    await update.message.reply_text(welcome_message)

# 🤖 الرد على أي رسالة
async def chat_with_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # لو المستخدم كتب أي حاجة فاضية أو رموز
    if not user_message.strip():
        await update.message.reply_text("قولّي أي حاجة أقدر أساعدك بيها 😅")
        return

    # استدعاء الذكاء الاصطناعي للرد
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # موديل خفيف وسريع
            messages=[
                {"role": "system", "content": "انت بوت ظريف ودمك خفيف بتتكلم باللهجة المصرية، بتمثل شركة أبو جو للتطوير الفضائي والسوفت وير والأدوات الصحية."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200,
            temperature=0.8
        )

        reply = response.choices[0].message.content.strip()

        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("حصل خطأ بسيط يا نجم 😅 جرب تاني كده بعد دقيقة.")

# 🛠️ بدء البوت
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # أوامر
    app.add_handler(CommandHandler("start", start))

    # أي رسالة (حتى من غير /start)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_ai))

    print("🚀 البوت اشتغل خلاص... جاهز للانطلاق!")
    app.run_polling()

if __name__ == "__main__":
    main()
