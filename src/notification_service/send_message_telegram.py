import requests
from datetime import datetime

from src.google_sheet.utils import update_today_sheet
from src.notification_service.config import BOT_TOKEN, CHAT_ID

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    #send html message
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}

    response = requests.post(url, json=payload)
    return response.json()

def notify_tasks_for_today():
    today = datetime.now().strftime('%Y-%m-%d')
    tasks,sheed_url = update_today_sheet()

    message = f"<b>Tasks for today</b>\n"
    if tasks.empty:
        message += "No tasks for today."
    else:
        for index, row in tasks.iterrows():
            message += f"&#8226; <i>{row['Title']}</i> (Due: <u>{row['Due Date']}</u>)\n"
    message += f"\n<i>More detail at <a href ='{sheed_url}'>here</a>. Have a productive day!</i>"
    send_message(CHAT_ID, message)

if __name__ == "__main__":
    notify_tasks_for_today()