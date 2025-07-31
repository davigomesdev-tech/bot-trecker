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
HORARIOS = [300, 700, 1200, 1800, 2200]

OFFERTS = [
    {
        "nome": "Celulite",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=335926936275636",
        "page_link": "https://celulitezero.net/" 
    },
    {
        "nome": "Reconquistar Ex",
        "status": "pre escala",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=252273351310701",
        "page_link": "https://www.metodocontrolatumente.com/mp1/" 
    },
    {
        "nome": "Mulher boa",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=679592661909218",
        "page_link": "https://seashell-goldfish-940501.hostingersite.com/1/" 
    },
    {
        "nome": "Mulher boa2",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=101991499536048",
        "page_link": "https://secret69.store/l/" 
    },
    {
        "nome": "Nutra Cabelo",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=674786479055567",
        "page_link": "https://esteticaparatodas.shop/p/belli" 
    },
    {
        "nome": "cigarro",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=721482367712433",
        "page_link": "https://quiz.cakto.com.br/preview/vicios-cigarro-ZwdoLv" 
    },
    {
        "nome": "mascara caseira",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=673803612486775",
        "page_link": "https://tudoonlinee360.com.br/" 
    },
    {
        "nome": "Lotofacil AI",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=718446011347059",
        "page_link": "https://resgatedigital.space/sorteloto/loto00/" 
    },
    {
        "nome": "Morango 1",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=356454970894276",
        "page_link": "https://uptqmonm.manus.space/"
    },
    {
        "nome": "Divivas",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=676857195511268",
        "page_link": "https://quiz.cakto.com.br/o-segredo-MOxnLO"
    },
    {
        "nome": "Morango 2",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=734673666398712",
        "page_link": "https://amor-perfeito-landing-31.lovable.app/"
    },
    {
        "nome": "seducao",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=705013096028486",
        "page_link": "https://institutoespecialista.com/1-quiz-seducao/"
    },
    {
        "nome": "Doces",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=701386549726656",
        "page_link": "https://osdocescaramelizados.xpages.co/"
    },
    {
        "nome": "reconstrução labial",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=703848672818293",
        "page_link": "https://lp.mychellemelo.site/"
    },
    {
        "nome": "morango 3",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=328733530313189",
        "page_link": "https://morango-do-amor-lucrativo.lovable.app/"
    },
    {
        "nome": "dor cerebro",
        "status": "validação",
        "lib_link": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&search_type=page&view_all_page_id=264184400116012",
        "page_link": "https://quiz.cakto.com.br/preview/estagio-de-cronificacao-fYxIiY"
    }
    
    # adicione mais ofertas aqui
]

def job():
    now = datetime.datetime.now()
    print(f"[INFO] Rodando job em {now.strftime('%Y-%m-%d %H:%M:%S')}")

    header = now.strftime('%d/%m - %H:%M')

    for off in OFFERTS:
        qtd = count_active_ads(off["lib_link"])
        upsert_offer(sheet, off, str(qtd), header)

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
