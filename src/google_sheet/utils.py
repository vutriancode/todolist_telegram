import pandas as pd
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

from src.google_sheet.config import *



# Kết nối đến Google Sheets
def connect():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    # 2) Khởi tạo service cho Google Sheets
    googles_sheets_service = build('sheets', 'v4', credentials=credentials)
    drive_service = build('drive', 'v3', credentials=credentials)
    return googles_sheets_service, drive_service

#get task for today
def get_tasks_for_today():
    service, drive_service = connect()
    range_ = 'todolist'
    result = service.spreadsheets().values().get(
        spreadsheetId=ALL_TODO_LIST_SPREADSHEET_ID, range=range_).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
        return None
    else:
        # Giả sử hàng đầu là header
        header = values[0]
        print(header)
        rows = values[1:]
        print(rows)
        today = datetime.utcnow() + timedelta(hours=7)
        today_string= today.strftime('%d/%m/%Y')
        today_dt = pd.to_datetime(today_string, format='%d/%m/%Y')
        df = pd.DataFrame(rows, columns=header)
        df['Date'] = pd.to_datetime(df['Due Date'], format='%d/%m/%Y')
        todolist_today = df[((df['Date'] >= today_dt) & (df['Recurrence'] == 'Daily')) | (df['Date'] == today_dt)]
        return todolist_today

#convert todolist frame to sheet accept type
def convert_todolist_to_sheet(todolist_today):
    todolist_today.drop(columns=['Worked_Time'], inplace=True)
    todolist_today.drop(columns=['Status'], inplace=True)
    todolist_today.drop(columns=['Date'], inplace=True)

    todolist_today['Status'] = 'Pending'
    todolist_today["Worked_time"] = 0
    todolist_today["Note"] = ""

    headers = todolist_today.columns.tolist()         # ['Name', 'Age']
    data = todolist_today.values.tolist()            # Dữ liệu từng row
    final_list = [headers] + data
    return final_list

# Tạo một Google Sheets mới
def create_new_spreadsheet_file(google_sheet_name):
    googles_sheets_service, drive_service = connect()
    spreadsheet_body = {
        'properties': {
            'title': google_sheet_name
        }
    }
    create_sheet_req = googles_sheets_service.spreadsheets().create(body=spreadsheet_body)
    create_sheet_res = create_sheet_req.execute()

    google_sheet_id = create_sheet_res['spreadsheetId']
    print(f"Created new Spreadsheet: {google_sheet_id}")
    return google_sheet_id


# Thêm file này vào một folder cụ thể trên Drive
def move_sheet_to_folder(google_sheet_id,folder_id):
    googles_sheets_service, drive_service = connect()
    update_req = drive_service.files().update(
        fileId=google_sheet_id,
        addParents=folder_id,  
        fields='id, parents'
    )
    update_res = update_req.execute()

    print("Updated parents (folder) for the new spreadsheet")

# Xóa một sheet
def clear_sheet(google_sheet_id, sheet_name):
    googles_sheets_service, drive_service = connect()
    clear_response = googles_sheets_service.spreadsheets().values().clear(
        spreadsheetId=google_sheet_id,
        range=sheet_name,
        body={}
    ).execute()
    print(f"Cleared data in range {sheet_name} of the spreadsheet {google_sheet_id}")
    return clear_response

# Tạo một sheet mới
def create_new_sheet(google_sheet_id, sheet_name):
    googles_sheets_service, drive_service = connect()
    requests_body = {
        "requests": [
            {
                "addSheet": {
                    "properties": {
                        "title": sheet_name
                        # Có thể thêm nhiều cấu hình khác như sheetType, gridProperties,...
                    }
                }
            }
        ]
    }

    response = googles_sheets_service.spreadsheets().batchUpdate(
        spreadsheetId=google_sheet_id,
        body=requests_body
    ).execute()
    print(f"Created new sheet: {sheet_name}")
    return response

def get_sheet_id_by_name(google_sheet_id, sheet_name):
    googles_sheets_service, drive_service = connect()
    spreadsheet = googles_sheets_service.spreadsheets().get(spreadsheetId=google_sheet_id).execute()
    sheets = spreadsheet.get('sheets', '')
    for sheet in sheets:
        properties = sheet.get('properties', '')
        title = properties.get('title', '')
        if title == sheet_name:
            sheet_id = properties.get('sheetId', '')
            return sheet_id
    return None

# add new rows to the sheet
def add_new_rows(google_sheet_id, sheet_name, data):
    googles_sheets_service, drive_service = connect()
    response = googles_sheets_service.spreadsheets().values().append(
        spreadsheetId=google_sheet_id,
        range=sheet_name,
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body={
            'values': data
        }
    ).execute()
    print(f"Added new rows to the sheet: {sheet_name}")
    return response

# Main function
def update_today_sheet():
    todolist_today = get_tasks_for_today()
    if todolist_today is None:
        return
    final_list = convert_todolist_to_sheet(todolist_today)
    today = datetime.utcnow() + timedelta(hours=7)
    today_string = today.strftime('%d/%m/%Y')
    try:
        clear_sheet(ALL_TODO_LIST_SPREADSHEET_ID, today_string)
    except Exception as e:
        create_new_sheet(ALL_TODO_LIST_SPREADSHEET_ID, today_string)
    add_new_rows(ALL_TODO_LIST_SPREADSHEET_ID, today_string, final_list)
    gid = get_sheet_id_by_name(ALL_TODO_LIST_SPREADSHEET_ID, today_string)
    sheed_url = f"https://docs.google.com/spreadsheets/d/{ALL_TODO_LIST_SPREADSHEET_ID}/edit#gid={gid}"
    return todolist_today,sheed_url

if __name__ == "__main__":
    update_today_sheet()