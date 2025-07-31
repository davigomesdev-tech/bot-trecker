import gspread
from oauth2client.service_account import ServiceAccountCredentials

def init_sheet(sheet_id, cred_json_path):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json_path, scope)
    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id).sheet1

def get_or_create_column(sheet, header_value):
    headers = sheet.row_values(1)
    if header_value in headers:
        return headers.index(header_value) + 1
    else:
        sheet.update_cell(1, len(headers) + 1, header_value)
        return len(headers) + 1

def find_row_by_offer(sheet, offer_name):
    col_values = sheet.col_values(1)  # coluna de nomes
    for i, name in enumerate(col_values[1:], start=2):  # pula header
        if name.strip().lower() == offer_name.strip().lower():
            return i
    return None

def upsert_offer(sheet, offer, value, header):
    col_index = get_or_create_column(sheet, header)
    row_index = find_row_by_offer(sheet, offer["nome"])

    if row_index:
        # Atualiza apenas a célula nova
        sheet.update_cell(row_index, col_index, value)
    else:
        # Cria nova linha com dados fixos + célula nova
        new_row = [
            offer["nome"],
            offer["status"],
            f'=HYPERLINK("{offer["lib_link"]}"; "biblioteca")',
            f'=HYPERLINK("{offer["page_link"]}"; "página de vendas")'
        ]
        current_headers = sheet.row_values(1)
        num_empty = len(current_headers) - len(new_row)
        new_row += [""] * num_empty
        if col_index > len(current_headers):
            new_row += [""] * (col_index - len(new_row))
        new_row[col_index - 1] = value
        sheet.append_row(new_row, value_input_option="USER_ENTERED")
