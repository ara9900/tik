from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = '386390730:AAGpxSWT88lyxUnjllBaESeEJRN5aF6-wPo'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("تست", callback_data='test')],
                [InlineKeyboardButton("خرید", callback_data='buy'),
                 InlineKeyboardButton("اشتراک های من", callback_data='my_subscriptions')],
                [InlineKeyboardButton("لیست قیمت ها", callback_data='price_list'),
                 InlineKeyboardButton("کیف پول", callback_data='wallet')],
                [InlineKeyboardButton("همکاری با ما", callback_data='collaborate'),
                 InlineKeyboardButton("تماس با پشتیبانی", callback_data='contact_support')],
                [InlineKeyboardButton("آموزش اتصال", callback_data='connect_tutorial'),
                 InlineKeyboardButton("راهنما", callback_data='help')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="لطفا یک گزینه را انتخاب کنید:",
                                   reply_markup=reply_markup)

app = ApplicationBuilder().token(TOKEN).build()

start_handler = CommandHandler('start', start)
app.add_handler(start_handler)

app.run_polling()
