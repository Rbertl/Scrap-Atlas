from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def realizar_pesquisas(driver: WebDriver, lista_de_dados: list):
    """
    Navega e realiza uma pesquisa para cada item na lista de dados.

    :param driver: A instância do WebDriver do Selenium já logada.
    :param lista_de_dados: Uma lista contendo os dados a serem pesquisados.
    """
    print("\n--- INICIANDO PROCESSO DE PESQUISA ---")
    url_base = "https://atlaseletro.my.site.com/NewAuthorizedCommunity/s/global-search/"
    
    wait = WebDriverWait(driver, 20)

    for dado in lista_de_dados:
        try:
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
                print("       Resultado correspondente encontrado! Clicando no link.")
                links_encontrados[0].click()
                
                print("       Aguardando carregamento da página de detalhes...")
                seletor_confirmacao = (By.XPATH, "//*[@field-label='Produto']")
                wait.until(EC.visibility_of_element_located(seletor_confirmacao))
                print("       Página de detalhes carregada.")

                try:
                    # =================================================================
                    # ### LÓGICA ALTERADA: CAPTURAR APENAS O PRIMEIRO RESULTADO ###
                    # =================================================================
                    
                    print("       Buscando pelo primeiro dado contendo 'FOGAO' na página...")
                    
                    # Seletor para encontrar qualquer elemento que contenha o texto
                    seletor_primeiro_fogao = (By.XPATH, "//*[contains(text(), 'FOGAO')]")
                    
                    # Usa o 'wait' para encontrar o PRIMEIRO elemento visível que corresponde.
                    # Se não encontrar em 20 segundos, ele vai gerar um erro (TimeoutException).
                    primeiro_elemento = wait.until(EC.visibility_of_element_located(seletor_primeiro_fogao))
                    
                    texto_extraido = primeiro_elemento.text.strip()
                    
                    if texto_extraido:
                        print(f"       >>> Primeiro resultado encontrado: {texto_extraido}")
                    else:
                        # Isso é raro, mas pode acontecer se o elemento estiver visível mas sem texto.
                        print("       !!! O primeiro elemento encontrado não continha texto visível.")

                except Exception as e_extracao:
                    # O erro mais comum aqui será TimeoutException se nada for encontrado.
                    print(f"       !!! Nenhum dado contendo 'FOGAO' foi encontrado na página.")

            else:
                print("       'Nenhum resultado' encontrado para este item.")
            
            print(f"[LOOP] Ações para '{dado}' concluídas.")

        except Exception as e:
            print(f"       !!! Ocorreu um erro ao pesquisar o item '{dado}': {e}")
            continue 
    
    print("\n--- PROCESSO DE PESQUISA FINALIZADO ---")