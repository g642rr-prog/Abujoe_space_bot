from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
import logging

logging.basicConfig(level=logging.DEBUG)

TOKEN = "8396425007:AAFz6k-o2iy6Ypo5SfAxcn1ryt2Ga1UwdEA"

# مراحل جمع البيانات
NAME, PHONE, CITY, CATEGORY, DETAILS = range(5)

# لوحة الخدمات
keyboard = [
    ['💻 برامج السوفت وير', '🚰 الأدوات الصحية', '🛠️ صيانة واستشارة']
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def start(update, context):
    update.message.reply_text("أهلاً بيك في *Abo Joe Space for Development* 🚀💫\n\nيلا نبدأ نسجّل طلبك 👇\n\n*اكتب اسمك كامل:*", parse_mode="Markdown")
    return NAME

def get_name(update, context):
    context.user_data["name"] = update.message.text
    update.message.reply_text("تمام يا باشا ✍️\n\nدلوقتي ابعتلي *رقم الواتساب*:", parse_mode="Markdown")
    return PHONE

def get_phone(update, context):
    context.user_data["phone"] = update.message.text
    update.message.reply_text("فين مكانك أو مدينتك؟ 🏙️")
    return CITY

def get_city(update, context):
    context.user_data["city"] = update.message.text
    update.message.reply_text("اختار نوع الخدمة 👇", reply_markup=reply_markup)
    return CATEGORY

def get_category(update, context):
    context.user_data["category"] = update.message.text
    update.message.reply_text("تمام ✅\n\nاكتبلي *التفاصيل / وصف طلبك* 📄", parse_mode="Markdown")
    return DETAILS

def get_details(update, context):
    context.user_data["details"] = update.message.text

    name = context.user_data["name"]
    phone = context.user_data["phone"]
    city = context.user_data["city"]
    category = context.user_data["category"]
    details = context.user_data["details"]

    msg = f"""
🚀 *تم تسجيل طلب جديد:*

👤 الاسم: {name}
📞 الواتساب: {phone}
🏙️ المدينة: {city}
🔧 نوع الخدمة: {category}
📄 التفاصيل:
{details}

سيتم التواصل معك قريبًا يا غالي ♥️
    """

    update.message.reply_text(msg, parse_mode="Markdown", reply_markup=reply_markup)
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text("تم الإلغاء ✋🙂")
    return ConversationHandler.END

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(Filters.text, get_name)],
        PHONE: [MessageHandler(Filters.text, get_phone)],
        CITY: [MessageHandler(Filters.text, get_city)],
        CATEGORY: [MessageHandler(Filters.text, get_category)],
        DETAILS: [MessageHandler(Filters.text, get_details)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)

dp.add_handler(conv_handler)
updater.start_polling()
print("🚀 البوت شغال يا كبير!")
