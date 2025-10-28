import os
import time
from config_selenium import SeleniumManager
from login.login import fazer_login
from dados.extrair_dados import obter_dados_para_pesquisa_pecas, salvar_dados_pesquisados_pecas
from pesquisa.valores_pesquisa import realizar_pesquisa_valores

def iniciar_automacao_pecas(caminho_planilha, log_callback, cancel_event):
    """
    Função principal que orquestra a automação de PESQUISA DE PEÇAS.
    """
    log_callback("--- INICIANDO AUTOMAÇÃO DE PESQUISA DE PEÇAS ---")
    
    manager = SeleniumManager(headless=True, log_callback=log_callback) # Mude para headless=False para ver o navegador
    
    if not manager.driver:
        log_callback("!!! FALHA: WebDriver não foi inicializado.")
        return

    driver = manager.driver
    
    try:
        login_bem_sucedido = fazer_login(driver, log_callback) #
        
        if login_bem_sucedido:
            # Verifica se foi cancelado logo após o login
            if cancel_event.is_set():
                log_callback("Processo cancelado após o login.")
                return

            log_callback("\nLogin realizado com sucesso.")
            
            # --- FLUXO DE SCRAPING (ATIVADO) ---
            
            log_callback("Iniciando obtenção de dados da planilha de peças...") #
            dados_a_pesquisar = obter_dados_para_pesquisa_pecas(caminho_planilha, log_callback) #
             
            if dados_a_pesquisar:
                log_callback("Iniciando pesquisa de valores...") #
                # Chama a função de pesquisa (que ainda contém a lógica placeholder)
                resultados_finais = realizar_pesquisa_valores(driver, dados_a_pesquisar, log_callback, cancel_event) #
                
                # Só salva se não foi cancelado
                if not cancel_event.is_set(): #
                    log_callback("Salvando resultados das peças...") #
                    # Salva os resultados (placeholders 'Pendente') na planilha
                    salvar_dados_pesquisados_pecas(resultados_finais, caminho_planilha, log_callback) #
                else:
                    log_callback("Salvamento ignorado devido ao cancelamento.") #
            else:
                 log_callback("Nenhum dado encontrado na planilha para pesquisar.")

            log_callback("\nAutomação de peças concluída!") # Ajustei a mensagem final
            
            # --- FIM DO FLUXO ATIVADO ---

            time.sleep(2) # Pausa breve antes de fechar

        else:
            log_callback("\nO login falhou. O script não pode continuar.") #
            time.sleep(3)

    except Exception as e:
        log_callback(f"Ocorreu um erro inesperado na automação de peças: {e}") #
    finally:
        manager.close_driver() #