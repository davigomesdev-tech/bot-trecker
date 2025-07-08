from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, InvalidArgumentException
from bs4 import BeautifulSoup
import re
import time

def count_active_ads(lib_url):
    print(f"[INFO] Iniciando scraping para URL:\n{lib_url}\n")

    # Configura o navegador headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        # Tenta iniciar o ChromeDriver
        driver = webdriver.Chrome(options=options)
        print("[OK] ChromeDriver iniciado com sucesso.")
    except WebDriverException as e:
        print(f"[ERRO] Falha ao iniciar o ChromeDriver:\n{e}")
        return 0

    try:
        # Tenta acessar a URL
        driver.get(lib_url)
        print("[OK] Página carregada com sucesso.")
    except InvalidArgumentException as e:
        print(f"[ERRO] URL inválida:\n{e}")
        driver.quit()
        return 0
    except WebDriverException as e:
        print(f"[ERRO] Falha ao carregar a página:\n{e}")
        driver.quit()
        return 0

    # Aguarda o carregamento da página
    time.sleep(5)

    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        text = soup.get_text()

        # Debug: salva HTML em arquivo (opcional)
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        match = re.search(r'~?(\d+)\s+results', text)
        if match:
            print(f"[OK] Resultado encontrado: {match.group(1)} anúncios ativos.\n")
            return int(match.group(1))
        else:
            print("[AVISO] Nenhum resultado encontrado no texto da página.")
            return 0

    except Exception as e:
        print(f"[ERRO] Erro ao processar HTML:\n{e}")
        return 0
    finally:
        driver.quit()
        print("[INFO] Navegador encerrado.\n")
