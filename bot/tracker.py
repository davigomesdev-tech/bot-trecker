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
        "nome": "URINA",
        "status": "validação",
        "lib_link": "https://pt-br.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=113502231769915",
        "page_link": "https://testeincontinencia.lovable.app/" 
    },
    {
        "nome": "CRIANCA BIRRA",
        "status": "validação",
        "lib_link": "https://pt-br.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=482914468231490",
        "page_link": "https://formulaantiagressividade.com/bk-05/" 
    },
    {
        "nome": "CRIANCA LER",
        "status": "validação",
        "lib_link": "https://pt-br.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=424371080758149",
        "page_link": "https://kitccsmetodologia.fun/" 
    },
    {
        "nome": "EMAGRECER",
        "status": "validação",
        "lib_link": "https://pt-br.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=103642606062121",
        "page_link": "https://seca-jejum.shop/" 
    },
    {
        "nome": "SEGREDO SEDUÇÃO",
        "status": "validação",
        "lib_link": "https://pt-br.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=639846659201654",
        "page_link": "https://www.expertpro.digital/OCAMINHODOHOMEM/" 
    },
    {
        "nome": "CORRER",
        "status": "validação",
        "lib_link": "https://pt-br.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=637914482733346",
        "page_link": "https://speedrunacademy.xpages.co/"
    },
    {
        "nome": "CHURRASCO",
        "status": "validação",
        "lib_link": "https://pt-br.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=773976339125020",
        "page_link": "https://churrasraiz.netlify.app/"
    },
    {
        "nome": "EMAGRWECER II",
        "status": "validação",
        "lib_link": "https://pt-br.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=420040031187109",
        "page_link": "https://www.vidaativa.online/VSL02"
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
