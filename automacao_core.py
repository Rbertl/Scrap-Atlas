import os
import time
from config_selenium import SeleniumManager
from login.login import fazer_login
from dados.extrair_dados import obter_dados_para_pesquisa, salvar_dados_pesquisados
from pesquisa.pesquisa import realizar_pesquisas

# A função agora aceita o 'cancel_event'
def iniciar_automacao(caminho_planilha, log_callback, cancel_event):
    """
    Função principal que orquestra a automação.
    """
    log_callback("--- INICIANDO AUTOMAÇÃO ATLAS ELETRODOMÉSTICOS ---")
    
    manager = SeleniumManager(headless=True, log_callback=log_callback)
    
    if not manager.driver:
        log_callback("!!! FALHA: WebDriver não foi inicializado. Verifique o chromedriver.exe e as configurações.")
        return

    driver = manager.driver
    
    try:
        login_bem_sucedido = fazer_login(driver, log_callback)
        
        if login_bem_sucedido:
            # Verifica se foi cancelado logo após o login
            if cancel_event.is_set():
                log_callback("Processo cancelado após o login.")
                return

            dados_a_pesquisar = obter_dados_para_pesquisa(caminho_planilha, log_callback)
            
            if dados_a_pesquisar:
                # Passa o 'cancel_event' para a função de pesquisa
                resultados_finais = realizar_pesquisas(driver, dados_a_pesquisar, log_callback, cancel_event)
                
                # Só salva se o processo não foi cancelado (resultados podem estar incompletos)
                if not cancel_event.is_set():
                    salvar_dados_pesquisados(resultados_finais, caminho_planilha, log_callback)
                else:
                    log_callback("Salvamento ignorado devido ao cancelamento.")

            log_callback("\nAutomação concluída com sucesso!")
            time.sleep(2)
        else:
            log_callback("\nO login falhou. O script não pode continuar.")
            time.sleep(3)

    except Exception as e:
        log_callback(f"Ocorreu um erro inesperado na automação principal: {e}")
    finally:
        manager.close_driver()