from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import logging
import requests

logging.basicConfig(level=logging.DEBUG)

TOKEN = "التوكن_اللي_شغال_عندك"

# حالات المحادثة
MAIN_MENU, PRODUCT_SELECTION, COLOR_SELECTION, FINAL_CONFIRMATION = range(4)

# بيانات المنتجات مع صور
products_data = {
    '🛁 حوض': {
        'name': 'حوض تركي سحاب',
        'price': 1200,
        'description': '🛁 حوض حمام تركي سحاب \n• ضمان 5 سنين \n• ألوان متعددة \n• تركيب مجاني',
        'image_url': 'https://example.com/hod.jpg',  # ضع لينك الصورة الحقيقي
        'colors': ['⚪ أبيض', '⚫ أسود', '🔵 أزرق', '🟤 بني']
    },
    '🚿 خلاط': {
        'name': 'خلاط تركي سحاب', 
        'price': 850,
        'description': '🚿 خلاط تركي سحاب \n• ضمان 5 سنين \n• توفير 40% مياه \n• تصميم أوروبي',
        'image_url': 'https://example.com/khallat.jpg',  # ضع لينك الصورة الحقيقي
        'colors': ['⚪ أبيض', '🔴 أحمر', '🔵 أزرق', '⚫ أسود']
    },
    '💎 بيديه': {
        'name': 'بيديه شاور',
        'price': 450,
        'description': '💎 بيديه شاور \n• ضمان 3 سنين \n• مقاوم للصدأ \n• تدفق قوي',
        'image_url': 'https://example.com/bideh.jpg',  # ضع لينك الصورة الحقيقي
        'colors': ['⚪ كروم', '⚫ أسود', '🟡 ذهبي']
    }
}

# لوحات المفاتيح الرئيسية
main_keyboard = [
    ['🚀 الخدمات الفضائية', '🚰 الأدوات الصحية'],
    ['📸 شوف المنتجات', '📞 كلمني مباشر'],
    ['🏢 اعرف عنا اكتر']
]

products_keyboard = [
    ['🛁 حوض', '🚿 خلاط', '💎 بيديه'],
    ['📸 شوف كل الصور', '🎥 فيديو المنتجات'],
    ['🏠 رجوع للرئيسية']
]

def start_bot(update, context):
    user = update.message.from_user
    welcome_text = f"""🚀 اهلا بيك في ابو جو للتطوير الفضائي! 😄

{user.first_name}.. قولي اخدمك ازاي ياعم الناس؟ 🙃

اختار من الأزرار تحت أو اكتب لي رسالة!"""
    
    update.message.reply_text(welcome_text, reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True))
    return MAIN_MENU

def handle_main_menu(update, context):
    user_text = update.message.text
    user = update.message.from_user
    
    if any(word in user_text for word in ['سلام', 'اهلا', 'اهلين', 'مرحبا', 'السلام', 'صباح', 'مساء', 'اهلًا']):
        response = f"وعليكم السلام 🌹\nازيك يافندم عامل ايه؟ 😃\n\n{user.first_name}.. اتفضل ازاي اقدر اساعدك او اخدمك؟"
        update.message.reply_text(response, reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True))
    
    elif user_text == '🚰 الأدوات الصحية':
        show_products(update, context)
        return PRODUCT_SELECTION
    
    elif user_text == '📸 شوف المنتجات':
        update.message.reply_text("🛍️ هوريك كل المنتجات الحلوة دي..")
        show_all_products(update, context)
        return PRODUCT_SELECTION
    
    elif user_text == '📞 كلمني مباشر':
        response = f"""📞 لأي حاجة تحتاجها.. {user.first_name}!

• 📞 01090285159
• 📞 01501763555  
• 📧 g642rr@gmail.com

⏰ 24 ساعة علشانك 👌

اختار من الأزرار تحت علشان نشوف المنتجات!"""
        update.message.reply_text(response, reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True))
    
    elif user_text == '🎥 فيديو المنتجات':
        # إرسال فيديو (ضع لينك فيديو حقيقي)
        update.message.reply_video(
            video="https://example.com/products_video.mp4",
            caption="🎥 شوف الفيديو ده علشان تعرف أكتر عن منتجاتنا!"
        )
        update.message.reply_text(
            "عجبك الفيديو؟ اختار منتج علشان تشوفه بالتفصيل! 👇",
            reply_markup=ReplyKeyboardMarkup(products_keyboard, resize_keyboard=True)
        )
        return PRODUCT_SELECTION
    
    else:
        response = f"{user.first_name}.. اتفضل ازاي اقدر اساعدك او اخدمك؟ 😊\n\nاختار من الأزرار تحت أو اكتب لي أي سؤال!"
        update.message.reply_text(response, reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True))
    
    return MAIN_MENU

def show_products(update, context):
    products_text = """🚰 أدواتنا الصحية:

• 🛁 أحواض حمامات تركية
• 🚿 خلاطات سحاب بضمان 5 سنين  
• 💎 بيديه شاور أوروبي

اختار منتج علشان تشوف صورته ومواصفاته! 👇"""
    
    update.message.reply_text(products_text, reply_markup=ReplyKeyboardMarkup(products_keyboard, resize_keyboard=True))

def show_all_products(update, context):
    """عرض كل المنتجات بالصور"""
    for product_key, product_data in products_data.items():
        try:
            # إرسال صورة المنتج
            update.message.reply_photo(
                photo=product_data['image_url'],
                caption=f"{product_key}: {product_data['description']}\n\nالسعر: {product_data['price']} جنيه 💰"
            )
        except:
            # لو الصورة مش شغالة، نرسل الوصف فقط
            update.message.reply_text(
                f"{product_key}: {product_data['description']}\n\nالسعر: {product_data['price']} جنيه 💰"
            )
    
    update.message.reply_text(
        "👆 دول كل المنتجات.. اختر اللي يعجبك!",
        reply_markup=ReplyKeyboardMarkup(products_keyboard, resize_keyboard=True)
    )

def handle_product_selection(update, context):
    user_text = update.message.text
    user = update.message.from_user
    
    if user_text in products_data:
        product_data = products_data[user_text]
        
        # إرسال صورة المنتج
        try:
            update.message.reply_photo(
                photo=product_data['image_url'],
                caption=f"{user_text}\n{product_data['description']}\n\nالسعر: {product_data['price']} جنيه 💰"
            )
        except:
            # لو الصورة مش شغالة
            update.message.reply_text(
                f"{user_text}\n{product_data['description']}\n\nالسعر: {product_data['price']} جنيه 💰"
            )
        
        # عرض ألوان المنتج
        colors_text = "🎨 اختر اللون اللي يعجبك:\n" + "\n".join(product_data['colors'])
        
        color_keyboard = [product_data['colors'][i:i+2] for i in range(0, len(product_data['colors']), 2)]
        color_keyboard.append(['↩ رجوع للمنتجات'])
        
        update.message.reply_text(
            colors_text,
            reply_markup=ReplyKeyboardMarkup(color_keyboard, resize_keyboard=True)
        )
        
        context.user_data['selected_product'] = product_data['name']
        context.user_data['price'] = product_data['price']
        
        return COLOR_SELECTION
    
    elif user_text == '📸 شوف كل الصور':
        show_all_products(update, context)
        return PRODUCT_SELECTION
    
    elif user_text == '🎥 فيديو المنتجات':
        update.message.reply_video(
            video="https://example.com/products_video.mp4",
            caption="🎥 شوف الفيديو ده علشان تعرف أكتر عن منتجاتنا!"
        )
        return PRODUCT_SELECTION
    
    elif user_text == '🏠 رجوع للرئيسية':
        return start_bot(update, context)
    
    else:
        # لو العميل كتب رسالة نصية
        response = f"{user.first_name}.. كلامك جميل! 🤝\n\nبس علشان أساعدك أحسن.. اختر من الأزرار تحت 👇"
        update.message.reply_text(response, reply_markup=ReplyKeyboardMarkup(products_keyboard, resize_keyboard=True))
        return PRODUCT_SELECTION

def handle_color_selection(update, context):
    user_text = update.message.text
    user = update.message.from_user
    
    if any(color in user_text for color in ['أبيض', 'أسود', 'أزرق', 'بني', 'أحمر', 'ذهبي', 'كروم']):
        context.user_data['color'] = user_text
        
        product = context.user_data.get('selected_product', 'منتج')
        price = context.user_data.get('price', 0)
        color = context.user_data.get('color', 'لون')
        
        response = f"""🎉 تمام.. اختيار رائع!

{user.first_name}.. الطلب النهائي:
• المنتج: {product}
• اللون: {color}  
• السعر: {price} جنيه
• الضمان: 5 سنين
• التركيب: مجاني 🤝

كلمنا على 01090285159 علشان نؤكد الطلب! 📞

أقدر أساعدك في حاجة تانية يافندم؟ 😊"""

        final_keyboard = [
            ['🛍 اطلب المنتج', '💳 استفسار عن التقسيط'],
            ['📸 شوف منتج تاني', '📞 كلمني مباشر'],
            ['🏠 إنهاء المحادثة']
        ]
        
        update.message.reply_text(response, reply_markup=ReplyKeyboardMarkup(final_keyboard, resize_keyboard=True))
        return FINAL_CONFIRMATION
    
    elif user_text == '↩ رجوع للمنتجات':
        show_products(update, context)
        return PRODUCT_SELECTION
    
    else:
        # لو العميل كتب رسالة
        response = f"{user.first_name}.. كلامك جميل! 💬\n\nبس علشان نكمل الطلب.. اختر اللون من الأزرار فوق 👆"
        update.message.reply_text(response)
        return COLOR_SELECTION

def handle_final_confirmation(update, context):
    user_text = update.message.text
    user = update.message.from_user
    
    if user_text == '🛍 اطلب المنتج':
        response = f"""🤝 تم استلام طلبك يا {user.first_name}!

هنتصل بيك خلال دقائق على 01090285159 علشان نؤكد التفاصيل 📞

شكراً لثقتك فينا! 🌷"""
        
        update.message.reply_text(response, reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True))
        return MAIN_MENU
    
    elif user_text == '📸 شوف منتج تاني':
        show_products(update, context)
        return PRODUCT_SELECTION
    
    elif user_text == '🏠 إنهاء المحادثة':
        response = f"شكراً لك يا {user.first_name}! 🌹\n\nمكانكم أي وقت تاني! 🙏"
        update.message.reply_text(response, reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True))
        return MAIN_MENU
    
    else:
        # لو العميل كتب أي رسالة
        response = f"{user.first_name}.. كلامك جميل وبنستفيد منه! 💭\n\nأقدر أساعدك في حاجة تانية؟ اختر من الأزرار 👇"
        update.message.reply_text(response, reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True))
        return MAIN_MENU

def handle_message(update, context):
    """لأي رسالة خارج المحادثة"""
    user = update.message.from_user
    response = f"يا {user.first_name}.. رجعلنا للقائمة الرئيسية علشان نكمل! 👇"
    update.message.reply_text(response, reply_markup=ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True))
    return MAIN_MENU

print("🚀 أبو جو للتطوير الفضائي شغال بنظام الأزرار والصور!")
updater = Updater(TOKEN, use_context=True)

conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.text & ~Filters.command, start_bot),
        CommandHandler('start', start_bot)
    ],
    states={
        MAIN_MENU: [MessageHandler(Filters.text & ~Filters.command, handle_main_menu)],
        PRODUCT_SELECTION: [MessageHandler(Filters.text & ~Filters.command, handle_product_selection)],
        COLOR_SELECTION: [MessageHandler(Filters.text & ~Filters.command, handle_color_selection)],
        FINAL_CONFIRMATION: [MessageHandler(Filters.text & ~Filters.command, handle_final_confirmation)],
    },
    fallbacks=[MessageHandler(Filters.text, handle_message)]
)

updater.dispatcher.add_handler(conv_handler)
updater.start_polling()
