import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN, ADMIN_IDS
from admin import admin_panel_handler, increase_user_wallet_handler
from database import cursor, conn
import admin  # این خط را اضافه کردیم
from admin import broadcast_message_prompt_handler, broadcast_message_handler


# ایجاد جدول کاربران در صورت عدم وجود
cursor.execute('''CREATE TABLE IF NOT EXISTS users
             (user_id INTEGER PRIMARY KEY,
             balance INTEGER DEFAULT 0)''')
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    username = update.effective_user.username

    try:
        # بررسی وجود کاربر در دیتابیس
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if not result:
            # اگر کاربر در دیتابیس وجود نداشت، اطلاعات کاربر را در دیتابیس ذخیره کنید
            cursor.execute("INSERT INTO users (user_id, first_name, last_name, username) VALUES (?, ?, ?, ?)",
                           (user_id, first_name, last_name, username))
            conn.commit()
            print(f"User {user_id} inserted into the database.")
        else:
            print(f"User {user_id} already exists in the database.")

    except sqlite3.Error as e:
        print(f"Error occurred while inserting user {user_id}: {e}")

    main_menu_keyboard = [[InlineKeyboardButton("تست💫", callback_data='test')],
                          [InlineKeyboardButton("خرید💵", callback_data='buy'),
                           InlineKeyboardButton("کیف پول💰", callback_data='wallet')],
                          [InlineKeyboardButton("لیست قیمت ها📑", callback_data='price_list'),
                           InlineKeyboardButton("اشتراک های من🟢", callback_data='my_subscriptions')],
                          [InlineKeyboardButton("همکاری با ما🤝🏻", callback_data='collaborate'),
                           InlineKeyboardButton("تماس با پشتیبانی🧑🏻‍💻", callback_data='contact_support')],
                          [InlineKeyboardButton("آموزش اتصال📚", callback_data='connect_tutorial'),
                           InlineKeyboardButton("راهنما💡", callback_data='help')]]
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="سلام به ربات تیک نت خوش اومدی❤️", reply_markup=reply_markup)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="لطفا یک گزینه را انتخاب کنید:",
                                       reply_markup=reply_markup)

async def wallet_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # دریافت موجودی کاربر از دیتابیس
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        balance = result[0]
    else:
        # اگر کاربر در دیتابیس وجود نداشت، یک ردیف جدید ایجاد کنید
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        balance = 0

    wallet_keyboard = [[InlineKeyboardButton("افزایش کیف پول", callback_data='increase_wallet')],
                       [InlineKeyboardButton("بازگشت به منوی اصلی", callback_data='start')]]
    wallet_reply_markup = InlineKeyboardMarkup(wallet_keyboard)
    await query.edit_message_text(text=f"موجودی شما: {balance} تومان", reply_markup=wallet_reply_markup)






app = ApplicationBuilder().token(TOKEN).build()

start_handler = CommandHandler('start', start)
wallet_handler = CallbackQueryHandler(wallet_menu, pattern='wallet')
back_to_main_handler = CallbackQueryHandler(start, pattern='start')

app.add_handler(start_handler)
app.add_handler(wallet_handler)
app.add_handler(back_to_main_handler)
app.add_handler(admin.admin_panel_handler)
app.add_handler(admin.increase_user_wallet_handler)
app.add_handler(admin.show_user_list_handler)  # این خط را اضافه کردیم
app.add_handler(broadcast_message_prompt_handler)
app.add_handler(broadcast_message_handler)

app.run_polling()

# بستن اتصال به دیتابیس
conn.close()
