from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchFrameException, NoSuchElementException

def realizar_pesquisa_valores(driver: WebDriver, lista_de_dados: list, log_callback=print, cancel_event=None):
    """
    Navega até a página de novo pedido de peças, entra no iframe,
    aguarda o carregamento, pesquisa cada código de peça e coleta descrição e valor,
    com espera aprimorada para conteúdo dinâmico.
    """
    log_callback("\n--- INICIANDO PESQUISA DE VALORES DE PEÇAS ---")
    
    url_novo_pedido = "https://atlaseletro.my.site.com/NewAuthorizedCommunity/s/novo-pedido-de-pecas"
    log_callback(f"Navegando para: {url_novo_pedido}")
    
    resultados_coletados = [] 
    iframe_focused = False 

    try:
        driver.get(url_novo_pedido)
        # Aumentar o tempo MÁXIMO de espera geral para elementos
        wait = WebDriverWait(driver, 45) # Aumentado para 45 segundos

        iframe_locator = (By.XPATH, "//iframe[@title='Contêiner de componente de Página do Visualforce']")
        
        log_callback("Aguardando e mudando para o iframe correto...")
        wait.until(EC.frame_to_be_available_and_switch_to_it(iframe_locator))
        iframe_focused = True 
        log_callback("Foco mudado para dentro do iframe.")
        
        seletor_div_confirmacao = (By.XPATH, "//div[contains(@class, 'slds-col') and contains(@class, 'slds-p-horizontal_medium') and normalize-space(text())='Pedido de Peças']")
        log_callback("Aguardando carregamento da div 'Pedido de Peças' dentro do iframe...")
        wait.until(EC.visibility_of_element_located(seletor_div_confirmacao)) 
        log_callback("Conteúdo do iframe carregado (div 'Pedido de Peças' encontrada).")

        input_codigo_locator = (By.ID, "part-code")
        input_nome_locator = (By.ID, "part-name")
        # --- ALTERAÇÃO SOLICITADA ---
        input_valor_locator = (By.XPATH, "(//input[@id='part-quantity'])[2]") # XPath para o SEGUNDO elemento com este ID
        # --- FIM DA ALTERAÇÃO ---

        # --- INÍCIO DO LOOP DE PESQUISA ---
        for dado in lista_de_dados:
            if cancel_event and cancel_event.is_set():
                log_callback("!!! PROCESSO CANCELADO PELO USUÁRIO !!!")
                break 

            log_callback(f"\n[LOOP] Pesquisando peça: {dado}")
            
            descricao_peca = "Não encontrado"
            valor_peca = "Não encontrado"
            
            try:
                # Usar um wait menor para encontrar o campo de código rapidamente
                campo_codigo = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(input_codigo_locator))
                
                campo_codigo.clear()
                # Pausa mínima antes de enviar as chaves
                time.sleep(0.3) 
                campo_codigo.send_keys(dado)
                log_callback(f"       Código '{dado}' inserido.")
                
                 # Pausa mínima antes de clicar fora
                time.sleep(0.4)
                div_confirmacao = driver.find_element(*seletor_div_confirmacao)
                ActionChains(driver).move_to_element(div_confirmacao).click().perform()
                log_callback("       Clicado fora do campo para iniciar a busca.")

                # --- ALTERAÇÃO NA ESPERA ---
                log_callback("       Aguardando descrição E valor da peça...")
                
                # Criar uma condição de espera customizada que verifica AMBOS os campos
                # Espera por até 20 segundos para ambos os campos terem valor
                WebDriverWait(driver, 20).until(
                    lambda d: d.find_element(*input_nome_locator).get_attribute('value').strip() != "" and \
                              d.find_element(*input_valor_locator).get_attribute('value').strip() != ""
                )
                
                # Pausa extra opcional após a espera ser satisfeita, caso a UI ainda esteja atualizando
                time.sleep(0.9) 
                # --- FIM DA ALTERAÇÃO NA ESPERA ---
                
                # Coletar descrição e valor
                campo_nome = driver.find_element(*input_nome_locator)
                descricao_peca = campo_nome.get_attribute('value').strip()
                
                # Coleta o valor usando o XPath modificado
                campo_valor = driver.find_element(*input_valor_locator) 
                valor_peca_raw = campo_valor.get_attribute('value').strip() 

                # --- FORMATAÇÃO DO VALOR ---
                try:
                    # Tenta converter para float (assumindo ponto decimal na coleta)
                    valor_float = float(valor_peca_raw)
                    # Formata para duas casas decimais e substitui ponto por vírgula
                    valor_peca = f"{valor_float:.2f}".replace('.', ',')
                except (ValueError, TypeError):
                    # Se a conversão falhar (valor não numérico ou vazio), mantém o valor bruto como resultado
                    log_callback(f"       Aviso: Não foi possível formatar o valor '{valor_peca_raw}' como moeda BRL.")
                    valor_peca = valor_peca_raw # Mantém o valor original (pode ser "", "Não encontrado", etc.)
                # --- FIM DA FORMATAÇÃO ---


                if not descricao_peca or not valor_peca: # Verifica se algum ficou vazio
                    if not descricao_peca: descricao_peca = "Descrição vazia"
                    if not valor_peca: valor_peca = "Valor não carregado"
                    log_callback("       !!! Descrição e/ou valor não preenchidos após a busca.")
                else:
                    log_callback(f"       >>> Descrição: {descricao_peca}")
                    log_callback(f"       >>> Valor: {valor_peca}")

            except TimeoutException:
                log_callback("       !!! Tempo esgotado esperando a descrição E/OU valor serem preenchidos. Peça pode não existir ou busca falhou.")
            except NoSuchElementException as e:
                log_callback(f"       !!! Erro ao encontrar um dos campos (código, nome ou valor): {e}")
            except Exception as e_loop:
                 log_callback(f"       !!! Erro inesperado ao processar o código '{dado}': {e_loop}")
                 descricao_peca = f"Erro no processamento"
                 valor_peca = f"Erro no processamento"
            
            resultados_coletados.append({'Codigo': dado, 'Descricao': descricao_peca, 'Valor': valor_peca})
            
             # Pausa entre as pesquisas para não sobrecarregar
            time.sleep(0.6) 
        # --- FIM DO LOOP ---

    except NoSuchFrameException:
        log_callback(f"!!! ERRO: Iframe com o localizador '{iframe_locator[1]}' não encontrado.")
        return []
    except TimeoutException:
        log_callback(f"!!! ERRO: Tempo esgotado esperando a div 'Pedido de Peças' dentro do iframe.") 
        return [] 
    except Exception as e:
        log_callback(f"!!! Ocorreu um erro inesperado antes do loop: {e}")
        return []
    finally:
        if iframe_focused:
            try:
                driver.switch_to.default_content()
                log_callback("Foco retornado ao conteúdo principal da página.")
            except Exception as e_switch:
                 log_callback(f"Aviso: Não foi possível retornar ao conteúdo principal. Erro: {e_switch}")

    log_callback("\n--- PESQUISA DE VALORES FINALIZADA ---")
    
    return resultados_coletados