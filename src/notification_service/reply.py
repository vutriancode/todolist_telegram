from datetime import datetime

from src.google_sheet.utils import update_today_sheet
from src.notification_service.config import BOT_TOKEN, CHAT_ID
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters


# Hàm xử lý tin nhắn nhận được
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lấy thông tin về chat
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    print(f"Nhận tin nhắn từ nhóm {chat_id}")
    print(f"Nhận tin nhắn từ nhóm {chat_type}")
    # Kiểm tra xem tin nhắn đến từ nhóm hay không
    if chat_type in ["group", "supergroup"] and chat_id == int(CHAT_ID):
        message_text = update.message.text
        print(f"Nhận tin nhắn từ nhóm {chat_id}: {message_text}")
        today = datetime.now().strftime('%Y-%m-%d')
        tasks,sheed_url = update_today_sheet()

        message = f"<b>Tasks for today</b>\n"
        if tasks.empty:
            message += "No tasks for today."
        else:
            for index, row in tasks.iterrows():
                message += f"&#8226; <i>{row['Title']}</i> (Due: <u>{row['Due Date']}</u>)\n"
        message += f"\n<i>More detail at <a href ='{sheed_url}'>here</a>. Have a productive day!</i>"

        # Ví dụ: bot trả lời lại trong nhóm
        await update.message.reply_text(f"{message}", parse_mode="HTML")

def main1():
    # while True:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handler cho tất cả tin nhắn văn bản (có thể từ nhóm hoặc cá nhân)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)

    application.run_polling()


import asyncio
main1()
