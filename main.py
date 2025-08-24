import os  # <-- NOVO: Importa o módulo 'os' para interagir com o sistema
from config_selenium import SeleniumManager
from login.login import fazer_login
from dados.extrair_dados import obter_dados_para_pesquisa
from pesquisa.pesquisa import realizar_pesquisas
import time

# =================================================================
# ### NOVA FUNÇÃO PARA LIMPAR O TERMINAL ###
# =================================================================
def limpar_terminal():
    """
    Limpa o console do terminal, compatível com Windows, Linux e macOS.
    """
    # Se o sistema operacional for Windows ('nt'), executa 'cls'
    if os.name == 'nt':
        os.system('cls')
    # Senão (para Linux e macOS, 'posix'), executa 'clear'
    else:
        os.system('clear')
# =================================================================

def iniciar_automacao():
    """
    Função principal que orquestra todo o processo de automação.
    """
    # ### ALTERAÇÃO 1: MODO HEADLESS ###
    # Alterado para True para rodar sem abrir a janela do navegador.
    manager = SeleniumManager(headless=True)
    driver = manager.driver
    
    try:
        # ETAPA 1: Executar o processo de login
        login_bem_sucedido = fazer_login(driver)
        
        if login_bem_sucedido:
            # ETAPA 2.1: Obter a lista de dados para pesquisar
            dados_a_pesquisar = obter_dados_para_pesquisa()
            
            # ETAPA 2.2: Iniciar o loop de pesquisas com os dados obtidos
            realizar_pesquisas(driver, dados_a_pesquisar)

            print("\nAutomação concluída com sucesso!")
            time.sleep(2)

        else:
            print("\nO login falhou. O script não pode continuar e será encerrado.")

    except Exception as e:
        print(f"Ocorreu um erro inesperado na automação principal: {e}")
    finally:
        manager.close_driver()

# Ponto de entrada do script principal
if __name__ == "__main__":
    # ### ALTERAÇÃO 2: CHAMADA DA FUNÇÃO ###
    # Limpa o terminal logo no início da execução
    limpar_terminal()
    
    print("--- INICIANDO AUTOMAÇÃO ATLAS ELETRODOMÉSTICOS ---")
    iniciar_automacao()