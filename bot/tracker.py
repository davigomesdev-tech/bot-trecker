import os
import time
import datetime
import schedule
from scraper import count_active_ads
from sheets import init_sheet, upsert_offer
from dotenv import load_dotenv
from pytz import timezone

# Carrega variáveis do .env
load_dotenv()

SHEET_ID = os.getenv("SHEET_ID")
CRED_PATH = os.getenv("CRED_JSON_PATH")

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

sheet = init_sheet(SHEET_ID, CRED_PATH)

def job():
    now = datetime.datetime.now(timezone("America/Sao_Paulo"))
    header = now.strftime('%d/%m - %H:00')
    print(f"[INFO] Executando coleta: {header}")

    for off in OFFERTS:
        qtd = count_active_ads(off["lib_link"])
        upsert_offer(sheet, off, str(qtd), header)

# Horários específicos de coleta
horarios = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 18, 21, 0]

for h in horarios:
    schedule.every().day.at(f"{h:02d}:00").do(job)

print("[INFO] Bot de monitoramento iniciado.")

while True:
    schedule.run_pending()
    time.sleep(30)
