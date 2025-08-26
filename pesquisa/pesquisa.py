from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# ARQUIVO PARA COLETAR MODELO PELA SERIE
# A função agora aceita o 'log_callback' como um parâmetro
# A função agora aceita o 'cancel_event'
def realizar_pesquisas(driver: WebDriver, lista_de_dados: list, log_callback=print, cancel_event=None):
    """
    Navega, realiza uma pesquisa e retorna os resultados coletados, verificando
    o sinal de cancelamento a cada iteração.
    """
    log_callback("\n--- INICIANDO PROCESSO DE PESQUISA ---")
    # ... (código da função sem alterações até o loop) ...
    url_base = "https://atlaseletro.my.site.com/NewAuthorizedCommunity/s/global-search/"
    wait = WebDriverWait(driver, 20)
    resultados_coletados = []

    for dado in lista_de_dados:
        # ### VERIFICAÇÃO DE CANCELAMENTO ###
        # A primeira coisa que o loop faz é checar o sinal.
        if cancel_event and cancel_event.is_set():
            log_callback("!!! PROCESSO CANCELADO PELO USUÁRIO !!!")
            break # Interrompe o loop 'for' imediatamente

        texto_final = "Não encontrado"
        try:
            # ... (toda a lógica de pesquisa, clique e extração continua a mesma) ...
            url_pesquisa = url_base + str(dado)
            log_callback(f"\n[LOOP] Pesquisando por: {dado}")
            log_callback(f"       Navegando para: {url_pesquisa}")
            driver.get(url_pesquisa)
            seletor_resultado_link = (By.XPATH, f"//a[normalize-space()='{dado}']")
            seletor_sem_resultado = (By.XPATH, "//*[contains(text(), 'Nenhum resultado')]")
            log_callback("       Aguardando resultado da pesquisa...")
            wait.until(
                lambda d: d.find_elements(*seletor_resultado_link) or d.find_elements(*seletor_sem_resultado)
            )
            log_callback("       Página de pesquisa carregada.")
            links_encontrados = driver.find_elements(*seletor_resultado_link)

            if links_encontrados:
                log_callback("       Resultado correspondente encontrado! Clicando no link.")
                links_encontrados[0].click()
                log_callback("       Aguardando carregamento da página de detalhes...")
                seletor_confirmacao = (By.XPATH, "//*[@field-label='Produto']")
                wait.until(EC.visibility_of_element_located(seletor_confirmacao))
                log_callback("       Página de detalhes carregada.")

                try:
                    seletor_primeiro_fogao = (By.XPATH, "//*[contains(text(), 'FOGAO')]")
                    primeiro_elemento = wait.until(EC.visibility_of_element_located(seletor_primeiro_fogao))
                    texto_extraido = primeiro_elemento.text.strip()
                    if texto_extraido:
                        log_callback(f"       >>> Primeiro resultado encontrado: {texto_extraido}")
                        texto_final = texto_extraido
                except Exception as e_extracao:
                    log_callback(f"       !!! Nenhum dado contendo 'FOGAO' foi encontrado na página.")
                    texto_final = "FOGAO não encontrado"
            else:
                log_callback("       'Nenhum resultado' encontrado para este item.")
                texto_final = "Item não localizado"
        except Exception as e:
            log_callback(f"       !!! Ocorreu um erro ao pesquisar o item '{dado}': {e}")
            texto_final = f"Erro no processamento"
        
        resultados_coletados.append({'Serie': dado, 'Modelo': texto_final})
        log_callback(f"[LOOP] Ações para '{dado}' concluídas.")
    
    log_callback("\n--- PROCESSO DE PESQUISA FINALIZADO ---")
    return resultados_coletados