# admin.py

import sqlite3
import io
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from config import ADMIN_IDS
from database import cursor, conn

async def is_admin(user_id):
    return user_id in ADMIN_IDS

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if await is_admin(user_id):
        # کاربر ادمین است، پنل ادمین را نمایش دهید
        admin_keyboard = [[InlineKeyboardButton("افزایش موجودی کاربر", callback_data='increase_user_wallet')],
                          [InlineKeyboardButton("مدیریت کاربران", callback_data='manage_users')],
                          [InlineKeyboardButton("لیست کاربران", callback_data='show_user_list')]]
        admin_reply_markup = InlineKeyboardMarkup(admin_keyboard)
        await update.message.reply_text("به پنل ادمین خوش آمدید.", reply_markup=admin_reply_markup)
    else:
        # کاربر ادمین نیست، پیام عدم دسترسی را نمایش دهید
        await update.message.reply_text("شما دسترسی به پنل ادمین را ندارید.")

async def increase_user_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if await is_admin(user_id):
        # بررسی اینکه آیا کاربر ادمین است یا خیر
        target_user_id = None
        try:
            # استخراج شناسه کاربر مورد نظر از کوئری
            target_user_id = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            # در صورت نامعتبر بودن شناسه کاربر، پیام خطا نمایش داده می‌شود
            await query.edit_message_text("شناسه کاربر نامعتبر است. لطفاً یک شناسه کاربر معتبر وارد کنید.")
            return

        if target_user_id:
            # اگر شناسه کاربر معتبر باشد
            amount = 1000  # مقدار افزایش موجودی

            try:
                # بررسی وجود کاربر در دیتابیس
                cursor.execute("SELECT * FROM users WHERE user_id = ?", (target_user_id,))
                user = cursor.fetchone()

                if user:
                    # اگر کاربر در دیتابیس وجود داشته باشد
                    # افزایش موجودی کاربر
                    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, target_user_id))
                    conn.commit()

                    # دریافت موجودی جدید کاربر از دیتابیس
                    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (target_user_id,))
                    result = cursor.fetchone()

                    balance = result[0]
                    # نمایش پیام موفقیت با موجودی جدید کاربر
                    await query.edit_message_text(f"موجودی کاربر با شناسه {target_user_id} با موفقیت {amount} تومان افزایش یافت.\nموجودی فعلی کاربر: {balance} تومان")
                else:
                    # اگر کاربر در دیتابیس وجود نداشته باشد
                    await query.edit_message_text(f"کاربر با شناسه {target_user_id} در دیتابیس یافت نشد.")

            except sqlite3.Error as e:
                # در صورت بروز خطا در هنگام افزایش موجودی کاربر
                print(f"Error occurred while increasing wallet for user {target_user_id}: {e}")
                await query.edit_message_text("خطایی در هنگام افزایش موجودی کاربر رخ داد. لطفاً بعداً دوباره امتحان کنید.")
        else:
            # اگر شناسه کاربر وارد نشده باشد
            await query.edit_message_text("لطفاً شناسه کاربر مورد نظر را وارد کنید.")
    else:
        await query.edit_message_text("شما دسترسی به این عملیات را ندارید.")
        
        

async def show_user_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("show_user_list function called")
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    print(f"User ID: {user_id}")

    if await is_admin(user_id):
        print("User is admin")
        try:
            cursor.execute("SELECT user_id FROM users")
            user_list = cursor.fetchall()
            print(f"User list: {user_list}")

            user_list_text = "لیست کاربران:\n\n"
            for user in user_list:
                user_id = user[0]
                user_list_text += str(user_id) + "\n"
                print(f"User ID: {user_id}")

            await query.edit_message_text(user_list_text)

        except sqlite3.Error as e:
            print(f"Error occurred while fetching user list: {e}")
            await query.edit_message_text("خطایی در هنگام دریافت لیست کاربران رخ داد. لطفاً بعداً دوباره امتحان کنید.")
    else:
        print("User is not admin")
        await query.edit_message_text("شما دسترسی به این عملیات را ندارید.")

admin_panel_handler = CommandHandler('panel', admin_panel)
increase_user_wallet_handler = CallbackQueryHandler(increase_user_wallet, pattern='^increase_user_wallet_')
show_user_list_handler = CallbackQueryHandler(show_user_list, pattern='show_user_list')
