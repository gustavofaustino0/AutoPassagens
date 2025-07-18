from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bot import enviar_mensagem
import time

# Iniciando tempo de execução
inicio = time.time()

# Configurações para rodar o Chrome em segundo plano (modo headless)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Roda o Chrome sem abrir a janela
chrome_options.add_argument("--disable-gpu")  # Desativa aceleração gráfica
chrome_options.add_argument(
    "--window-size=1920,1080"
)  # Tamanho da janela (mesmo sem exibição)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

menor_preco = 999999999
while True:
    navegador = webdriver.Chrome(options=chrome_options)
    navegador.get("https://www.vaidepromo.com.br/")

    # Origem
    botao_origem = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[data-cy="departure"]'))
    )
    botao_origem.click()
    botao_origem.send_keys("Salvador")

    time.sleep(2)

    botao_origem = navegador.find_element(By.CSS_SELECTOR, 'button[value="SSA"]')
    botao_origem.click()

    # Destino

    botao_destino = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[data-cy="arrival"]'))
    )
    botao_destino.click()
    botao_destino.send_keys("Porto Alegre")

    time.sleep(2)

    botao_destino = navegador.find_element(By.CSS_SELECTOR, 'button[value="POA"]')
    botao_destino.click()

    time.sleep(5)

    # Data de origem
    data_origem = navegador.find_element(
        By.CSS_SELECTOR,
        "div._container_1qwfw_1._departureDateInput_1b8ol_25._inputDesktop_c5hg9_11",
    )
    data_origem.click()

    time.sleep(5)

    for i in range(4):
        data_origem = navegador.find_element(
            By.XPATH, "//button[@data-cy='data-range-picker-next']"
        )
        time.sleep(1)
        data_origem.click()

    data_origem = navegador.find_element(By.XPATH, "//button[@data-cy='13-12-2025']")
    data_origem.click()

    # Data de Destino
    time.sleep(1)

    data_destino = navegador.find_element(
        By.XPATH, '//button[@data-testid="17-12-2025"]'
    )
    data_destino.click()

    # Pesquisar

    search = navegador.find_element(
        By.XPATH, '//button[@data-cy="submit-search-button"]'
    )
    search.click()

    time.sleep(15)

    # Preços

    preco_atual = navegador.find_element(
        By.XPATH, "//strong[text()='Preço total']/following-sibling::strong"
    )

    # Conversão de String pra Inteiro

    preco_int = int(
        float(
            preco_atual.text.replace("R$", "")
            .replace(".", "")
            .replace(",", ".")
            .strip()
        )
    )

    # Link da Compra

    link_element = navegador.find_element(
        By.CSS_SELECTOR, "a[data-cy='comprar-button']"
    )

    link_resultado = link_element.get_attribute("href")

    # Enviar Mensagem

    if preco_int < menor_preco:
        menor_preco = preco_int
        mensagem = f"""
✈️ <b>Menor valor de passagens encontradas!</b> ✈️

➡️ <b>Ida:</b> 13/12/2025 🛫  
⬅️ <b>Volta:</b> 17/12/2025 🛬  

💰 <b>Total ida e volta:</b> R$ {menor_preco} 💸

🎉 Reserve já sua viagem e aproveite esses preços incríveis!  
👉 <a href="{link_resultado}">Compre aqui</a> 🌍
"""

        enviar_mensagem(mensagem)

    # Tempo de execução
    tempo_decorrido = time.time() - inicio

    horas = int(tempo_decorrido // 3600)
    minutos = int((tempo_decorrido % 3600) // 60)
    segundos = int(tempo_decorrido % 60)

    print(f"Tempo de execução: {horas}h {minutos}min {segundos}s")
    navegador.quit()

    time.sleep(300)
