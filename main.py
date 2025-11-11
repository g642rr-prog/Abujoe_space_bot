# ----------------- main_fixed.py — Abo Joe Bot (friendly seller, OpenAI with real error logging) -----------------
import os
import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)
from openai import OpenAI, error

# ----------------- CONFIG -----------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise RuntimeError("Missing TELEGRAM_TOKEN in environment variables.")
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in environment variables.")

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AboJoeBot")

# ----------------- Keyboard -----------------
MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["🛠 صيانة / سوفت وير", "🚰 أدوات صحية"],
        ["🛰 منتجات وقطع غيار", "💬 أتكلّم مع الدعم"],
        ["🏢 عن أبو جو"]
    ],
    resize_keyboard=True
)

# ----------------- Utility helpers -----------------
def short_system_prompt():
    return (
        "You are 'Abo Joe' — a friendly Egyptian seller and tech helper. "
        "Keep tone warm, slightly joking but respectful, helpful, brief when needed. "
        "When a user asks about products, ask clarifying questions (budget, usage, brand preference). "
        "For casual chit-chat, reply playfully but guide the conversation to offer help."
    )

async def call_openai_chat(user_text: str) -> str:
    try:
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": short_system_prompt()},
                {"role": "user", "content": user_text}
            ],
            max_tokens=350
        )
        return resp.choices[0].message.content.strip()
    except error.OpenAIError as e:
        # Catch OpenAI-specific errors
        logger.exception("OpenAI API error")
        return f"يا معلم حصلت مشكلة في الدماغ الصناعي عندي: {str(e)} 😅"
    except Exception as e:
        # Catch any other errors
        logger.exception("Unexpected error in OpenAI call")
        return f"يا معلم حصلت مشكلة غير متوقعة: {str(e)} 😅"

# ----------------- Conversation helpers -----------------
def set_state(context: ContextTypes.DEFAULT_TYPE, key: str, value):
    context.user_data[key] = value

def get_state(context: ContextTypes.DEFAULT_TYPE, key: str, default=None):
    return context.user_data.get(key, default)

def clear_state(context: ContextTypes.DEFAULT_TYPE, *keys):
    for k in keys:
        if k in context.user_data:
            del context.user_data[k]

# ----------------- Handlers -----------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"🚀 أهلاً بيك يا {user.first_name} في *أبو جو للتطوير الفضائي*! \n\n"
        "أنا معاك ومش هسيبك غير وإنت مبسوط 🙃\n"
        "قولي أخدمك ازاي يا باشا؟ 😄"
    )
    await update.message.reply_text(text, reply_markup=MAIN_KEYBOARD, parse_mode="Markdown")
    clear_state(context)  # reset any previous flow

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    lower = text.lower()

    # زرار من المينيو
    if text == "🛠 صيانة / سوفت وير":
        set_state(context, "flow", "service")
        await update.message.reply_text(
            "تمام يا جميل 🤝\nإنت بتدور على خدمة صيانة ولا عايز سوفت وير جديد يتظبط للشغل؟\n"
            "ابعتلي جملة قصيرة عن المطلوب، أو قول: *عايز مساعدة اختيار*",
            reply_markup=MAIN_KEYBOARD,
            parse_mode="Markdown"
        )
        return

    if text == "🚰 أدوات صحية":
        set_state(context, "flow", "sanitary")
        await update.message.reply_text(
            "حلو قوي! قطاع الأدوات الصحية 👍\nقولي: بتجهز بيت جديد ولا تجديد؟ أو ابعتلي صورة للمكان لو تحب.",
            reply_markup=MAIN_KEYBOARD
        )
        return

    if text == "🛰 منتجات وقطع غيار":
        set_state(context, "flow", "parts")
        await update.message.reply_text(
            "نقطة لصالحك 👌\nبتدور على نوع معين ولا تحب أقولك أشهر الحاجات اللي عندنا؟",
            reply_markup=MAIN_KEYBOARD
        )
        return

    if text == "💬 أتكلّم مع الدعم":
        clear_state(context)
        await update.message.reply_text(
            "طيب يا باشا 👌 ابعتلي اسمك ورقمك وهبعته لفريق الدعم يتواصل معاك فوراً.",
            reply_markup=MAIN_KEYBOARD
        )
        set_state(context, "awaiting_contact", True)
        return

    if text == "🏢 عن أبو جو":
        await update.message.reply_text(
            "🏢 أبو جو للتطوير الفضائي — سوفت وير، أدوات صحية، و خدمة بعد البيع جدعة 👏\nنورتنا 🌷",
            reply_markup=MAIN_KEYBOARD
        )
        return

    # لو مستني بيانات اتصال
    if get_state(context, "awaiting_contact"):
        name = update.effective_user.first_name
        chat_id = update.effective_chat.id
        set_state(context, "contact_info", {"name": name, "chat_id": chat_id, "message": text})
        clear_state(context, "awaiting_contact")
        await update.message.reply_text("تمام يا بطل 👍 الفريق استلم بياناتك وهنتواصل معاك قريباً.", reply_markup=MAIN_KEYBOARD)
        return

    # لو في فلتر flow
    current_flow = get_state(context, "flow")
    if current_flow in ("service", "sanitary", "parts"):
        if not get_state(context, "clarified"):
            set_state(context, "clarified", True)
            set_state(context, "expecting_budget", True)
            set_state(context, "last_user_text", text)
            await update.message.reply_text(
                "جميل يا معلم 👍\nقبل ما أرشّحلك أحسن حاجة: تقولي تقريباً ميزانيتك قد إيه؟",
                reply_markup=MAIN_KEYBOARD
            )
            return

        if get_state(context, "expecting_budget"):
            set_state(context, "budget", text)
            clear_state(context, "expecting_budget")
            set_state(context, "expecting_usage", True)
            await update.message.reply_text(
                f"تمام، ميزانيتك تقريباً: *{text}* ✅\n\nطيب الاستخدام؟ (بيت جديد / تجديد / محل تجاري / صناعي ؟)",
                parse_mode="Markdown",
                reply_markup=MAIN_KEYBOARD
            )
            return

        if get_state(context, "expecting_usage"):
            set_state(context, "usage", text)
            clear_state(context, "expecting_usage")
            user_brief = get_state(context, "last_user_text") or "مطلوب"
            budget = get_state(context, "budget")
            usage = get_state(context, "usage")
            prompt = (
                f"العميل طلب: {user_brief}\n"
                f"ميزانية: {budget}\n"
                f"الاستخدام: {usage}\n"
                "اقترح 3 خيارات: (1) ممتاز (2) متوسط السعر (3) اقتصادي. "
                "كل خيار سطر واحد مع اقتراح سؤال متابعة."
            )
            ai_reply = await call_openai_chat(prompt)
            set_state(context, "last_suggestion", ai_reply)
            await update.message.reply_text(
                f"حضرتك تمام يا باشا 👇\n\n{ai_reply}\n\nعايز أبعتلك صور للكلام دا ولا تختار من اللي فوق؟",
                reply_markup=MAIN_KEYBOARD
            )
            clear_state(context, "flow")
            clear_state(context, "clarified")
            return

    # لو الكلام عام
    if text == "":
        await update.message.reply_text("يا عم اكتبلي حبة حاجة بسيطة عشان أقدر أساعدك 😅", reply_markup=MAIN_KEYBOARD)
        return

    prompt = f"User: {text}\nRespond as a friendly Egyptian seller (Abo Joe). Keep it short, helpful, and playful."
    ai_answer = await call_openai_chat(prompt)
    await update.message.reply_text(ai_answer, reply_markup=MAIN_KEYBOARD)

# ----------------- Entry point -----------------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    logger.info("🚀 Abo Joe Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
