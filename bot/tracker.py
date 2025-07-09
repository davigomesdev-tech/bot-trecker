import os, time, datetime
import schedule
from scraper import count_active_ads
from sheets import init_sheet, append_data
from dotenv import load_dotenv

load_dotenv('config.env')
SHEET_ID = os.getenv('SHEET_ID')
CRED_JSON = os.getenv('GOOGLE_CRED_JSON')

sheet = init_sheet(SHEET_ID, CRED_JSON)

# Defina aqui os horários (formato: HHMM)
HORARIOS = [0600, 1200, 1800]

OFFERTS = [
    {
        "nome": "Precoce",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=654061921118397",
        "page_link": "https://quiz.cakto.com.br/responda-EVxSYx"
    },
    {
        "nome": "Seca banha",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=743027218884835",
        "page_link": "https://54188.xpages.co/"
    },
    {
        "nome": "Astrologia",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=673055179221190",
        "page_link": "https://quiz.astrologiasemfirula.com/"
    },
    {
        "nome": "Gripe Filho",
        "status": "pre escala",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=108074855424424",
        "page_link": "https://xogripe.site/"
    },
    {
        "nome": "Pix Video",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=395600250311478",
        "page_link": "https://pixvideo.vercel.app/"
    }
    # adicione mais ofertas aqui
]

def job():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[INFO] Rodando job em {now}")
    row = []
    for off in OFFERTS:
        qtd = count_active_ads(off["lib_link"])
        row.extend([
            off["nome"],
            off["status"],
            f'=HYPERLINK("{off["lib_link"]}"; "biblioteca")',
            f'=HYPERLINK("{off["page_link"]}"; "página de vendas")',
            f"{now}",
            str(qtd)
        ])
    append_data(sheet, row)

# Agendar os horários definidos
for h in HORARIOS:
    hh = str(h).zfill(4)  # ex: 830 -> '0830'
    hora_formatada = f"{hh[:2]}:{hh[2:]}"  # '0830' -> '08:30'
    schedule.every().day.at(hora_formatada).do(job)
    print(f"[AGENDA] Job agendado para {hora_formatada}")

if __name__ == "__main__":
    print("[INFO] Bot iniciado e aguardando os horários programados...")
    while True:
        schedule.run_pending()
        time.sleep(1)
