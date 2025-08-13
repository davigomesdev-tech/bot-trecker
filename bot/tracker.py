import os
import time
import datetime
import schedule
from scraper import count_active_ads
from sheets import init_sheet, upsert_offer
from dotenv import load_dotenv
from pytz import timezone

load_dotenv('config.env')
SHEET_ID = os.getenv('SHEET_ID')
CRED_JSON = os.getenv('GOOGLE_CRED_JSON')

sheet = init_sheet(SHEET_ID, CRED_JSON)

# Defina aqui os horários (formato: HHMM)
HORARIOS = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1500, 1800, 2100, 0]

OFFERTS = [
    {
        "nome": "ALTAR",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=584683601389046",
        "page_link": "https://quiz.planyzo.com/" 
    }
    # ... mantenha as outras ofertas iguais
]

def job():
    now = datetime.datetime.now(timezone("America/Sao_Paulo"))
    header = now.strftime('%d/%m - %H:%M')
    print(f"[INFO] Rodando job em {header}")

    for off in OFFERTS:
        qtd = count_active_ads(off["lib_link"])
        upsert_offer(sheet, off, str(qtd), header)

# Agendar os horários definidos
for h in HORARIOS:
    hh = str(h).zfill(4)  # ex: 300 -> '0300'
    hora_formatada = f"{hh[:2]}:{hh[2:]}"  # '0300' -> '03:00'
    schedule.every().day.at(hora_formatada).do(job)
    print(f"[AGENDA] Job agendado para {hora_formatada}")

if __name__ == "__main__":
    print("[INFO] Bot iniciado e aguardando os horários programados...")
    while True:
        schedule.run_pending()
        time.sleep(1)
