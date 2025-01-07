import requests
from api.db import get_tasks_for_day
from datetime import datetime

# Telegram bot token and chat ID
BOT_TOKEN = '8115272386:AAE4YiBjiAp1U8Z0sMy09UTtIy5_DNJxjHA'
CHAT_ID = '-1002422021123'

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    #send html message
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}

    response = requests.post(url, json=payload)
    return response.json()

def notify_tasks_for_today():
    today = datetime.now().strftime('%Y-%m-%d')
    tasks = get_tasks_for_day(today)
    if tasks:
        message = "Tasks for today:\n"
        for task in tasks:
            message += f"- {task.title} (Due: {task.due_date})\n"
    else:
        message = "No tasks for today."
    message = f"<b>Tasks for today:</b>\n"
    for task in tasks:
        message += f"&#8226; <i>{task.title}</i> (Due: <u>{task.due_date}</u>)\n"
    message += "\n<i>Have a productive day!</i>"
    send_message(CHAT_ID, message)

if __name__ == "__main__":
    notify_tasks_for_today()