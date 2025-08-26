from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def realizar_pesquisas(driver: WebDriver, lista_de_dados: list):
    """
    Navega, realiza uma pesquisa e retorna os resultados coletados.
    """
    print("\n--- INICIANDO PROCESSO DE PESQUISA ---")
    url_base = "https://atlaseletro.my.site.com/NewAuthorizedCommunity/s/global-search/"
    wait = WebDriverWait(driver, 20)
    
    # Lista para armazenar os resultados
    resultados_coletados = []

    for dado in lista_de_dados:
        texto_final = "Não encontrado" # Valor padrão
        try:
            # ... (lógica de navegação e clique continua a mesma) ...
            url_pesquisa = url_base + str(dado)
            print(f"\n[LOOP] Pesquisando por: {dado}")
            print(f"       Navegando para: {url_pesquisa}")
            driver.get(url_pesquisa)
            seletor_resultado_link = (By.XPATH, f"//a[normalize-space()='{dado}']")
            seletor_sem_resultado = (By.XPATH, "//*[contains(text(), 'Nenhum resultado')]")
            print("       Aguardando resultado da pesquisa...")
            wait.until(
                lambda d: d.find_elements(*seletor_resultado_link) or d.find_elements(*seletor_sem_resultado)
            )
            print("       Página de pesquisa carregada.")
            links_encontrados = driver.find_elements(*seletor_resultado_link)

            if links_encontrados:
                # ... (lógica de clique e espera da página de detalhes continua a mesma) ...
                print("       Resultado correspondente encontrado! Clicando no link.")
                links_encontrados[0].click()
                print("       Aguardando carregamento da página de detalhes...")
                seletor_confirmacao = (By.XPATH, "//*[@field-label='Produto']")
                wait.until(EC.visibility_of_element_located(seletor_confirmacao))
                print("       Página de detalhes carregada.")

                try:
                    # Lógica de extração do primeiro resultado com 'FOGAO'
                    seletor_primeiro_fogao = (By.XPATH, "//*[contains(text(), 'FOGAO')]")
                    primeiro_elemento = wait.until(EC.visibility_of_element_located(seletor_primeiro_fogao))
                    texto_extraido = primeiro_elemento.text.strip()
                    if texto_extraido:
                        print(f"       >>> Primeiro resultado encontrado: {texto_extraido}")
                        texto_final = texto_extraido # Atualiza o valor a ser salvo
                except Exception as e_extracao:
                    print(f"       !!! Nenhum dado contendo 'FOGAO' foi encontrado na página.")
                    texto_final = "FOGAO não encontrado"
            else:
                print("       'Nenhum resultado' encontrado para este item.")
                texto_final = "Item não localizado"
        except Exception as e:
            print(f"       !!! Ocorreu um erro ao pesquisar o item '{dado}': {e}")
            texto_final = f"Erro: {e}"
        
        # Adiciona o resultado (sucesso ou falha) à nossa lista
        resultados_coletados.append({'Serie': dado, 'Modelo': texto_final})
        print(f"[LOOP] Ações para '{dado}' concluídas.")
    
    print("\n--- PROCESSO DE PESQUISA FINALIZADO ---")
    # Retorna a lista completa de resultados
    return resultados_coletados