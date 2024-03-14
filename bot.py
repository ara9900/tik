from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = '386390730:AAGpxSWT88lyxUnjllBaESeEJRN5aF6-wPo'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_menu_keyboard = [[InlineKeyboardButton("تست", callback_data='test')],
                          [InlineKeyboardButton("خرید", callback_data='buy'),
                           InlineKeyboardButton("کیف پول", callback_data='wallet')],
                          [InlineKeyboardButton("لیست قیمت ها", callback_data='price_list'),
                           InlineKeyboardButton("اشتراک های من", callback_data='my_subscriptions')],
                          [InlineKeyboardButton("همکاری با ما", callback_data='collaborate'),
                           InlineKeyboardButton("تماس با پشتیبانی", callback_data='contact_support')],
                          [InlineKeyboardButton("آموزش اتصال", callback_data='connect_tutorial'),
                           InlineKeyboardButton("راهنما", callback_data='help')]]
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="لطفا یک گزینه را انتخاب کنید:", reply_markup=reply_markup)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="لطفا یک گزینه را انتخاب کنید:",
                                       reply_markup=reply_markup)

async def wallet_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    wallet_keyboard = [[InlineKeyboardButton("افزایش کیف پول", callback_data='increase_wallet')],
                       [InlineKeyboardButton("بازگشت به منوی اصلی", callback_data='start')]]
    wallet_reply_markup = InlineKeyboardMarkup(wallet_keyboard)
    await query.edit_message_text(text="موجودی شما: 0 تومان", reply_markup=wallet_reply_markup)

app = ApplicationBuilder().token(TOKEN).build()

start_handler = CommandHandler('start', start)
wallet_handler = CallbackQueryHandler(wallet_menu, pattern='wallet')
back_to_main_handler = CallbackQueryHandler(start, pattern='start')

app.add_handler(start_handler)
app.add_handler(wallet_handler)
app.add_handler(back_to_main_handler)

app.run_polling()
