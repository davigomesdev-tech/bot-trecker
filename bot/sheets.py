import gspread
from oauth2client.service_account import ServiceAccountCredentials

HEADERS_FIXOS = ["Nome", "Status", "Biblioteca", "Página de Vendas"]

def init_sheet(sheet_id, cred_json_path):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).sheet1

    # Adiciona cabeçalho se estiver vazio
    if not sheet.row_values(1):
        sheet.append_row(HEADERS_FIXOS, value_input_option="USER_ENTERED")

    return sheet

def get_or_create_column(sheet, header_value):
    headers = sheet.row_values(1)
    if header_value in headers:
        return headers.index(header_value) + 1
    else:
        sheet.update_cell(1, len(headers) + 1, header_value)
        return len(headers) + 1

def find_row_by_offer(sheet, offer_name):
    col_values = sheet.col_values(1)
    for i, name in enumerate(col_values[1:], start=2):
        if name.strip().lower() == offer_name.strip().lower():
            return i
    return None

def upsert_offer(sheet, offer, value, header):
    col_index = get_or_create_column(sheet, header)
    row_index = find_row_by_offer(sheet, offer["nome"])

    if row_index:
        sheet.update_cell(row_index, col_index, value)
    else:
        new_row = [
            offer["nome"],
            offer["status"],
            f'=HYPERLINK("{offer["lib_link"]}"; "biblioteca")',
            f'=HYPERLINK("{offer["page_link"]}"; "página de vendas")'
        ]

        header_row = sheet.row_values(1)
        total_cols = len(header_row)

        while len(new_row) < total_cols:
            new_row.append("")

        new_row[col_index - 1] = value
        sheet.append_row(new_row, value_input_option="USER_ENTERED")
