import gspread
from oauth2client.service_account import ServiceAccountCredentials

def init_sheet(sheet_id, cred_json_path):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json_path, scope)
    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id).sheet1

def append_data(sheet, row_values):
    sheet.append_row(row_values, value_input_option='USER_ENTERED')

