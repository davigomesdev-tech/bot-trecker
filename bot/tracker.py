import os
import time
import datetime
import schedule
from scraper import count_active_ads
from sheets import init_sheet, upsert_offer
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

SHEET_ID = os.getenv('SHEET_ID')
CRED_JSON = os.getenv('GOOGLE_CRED_JSON')

# Lista de ofertas monitoradas
OFFERTS = [
    {
        "nome": "Celulite",
        "status": "validação",
        "lib_link": "https://seulink.com/lib1",
        "page_link": "https://seulink.com/page1"
    },
    {
        "nome": "Mulher Boa",
        "status": "validação",
        "lib_link": "https://seulink.com/lib2",
        "page_link": "https://seulink.com/page2"
    },
    # Adicione mais aqui
]

sheet = init_sheet(SHEET_ID, CRED_JSON)

def job():
    now = datetime.datetime.now(timezone("America/Sao_Paulo"))
    header = now.strftime('%d/%m - %H:00')
    print(f"[INFO] Executando coleta: {header}")

    for off in OFFERTS:
        qtd = count_active_ads(off["lib_link"])
        upsert_offer(sheet, off, str(qtd), header)

# Exemplo de horários com minutos: (hora, minuto)
horarios = [
    (3, 0),
    (4, 30)
]

for h, m in horarios:
    schedule.every().day.at(f"{h:02d}:{m:02d}").do(job)

print("[INFO] Bot de monitoramento iniciado.")

while True:
    schedule.run_pending()
    time.sleep(30)
