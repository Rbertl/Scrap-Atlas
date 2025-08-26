import os
import time
from config_selenium import SeleniumManager
from login.login import fazer_login
from dados.extrair_dados import obter_dados_para_pesquisa, salvar_dados_pesquisados
from pesquisa.pesquisa import realizar_pesquisas
from interface_usuario import selecionar_arquivo_planilha  # <-- NOVO IMPORT

def limpar_terminal():
    # ... (função sem alterações) ...
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def iniciar_automacao():
    """
    Função principal que orquestra todo o processo de automação.
    """
    # ### ALTERAÇÃO PRINCIPAL: SELEÇÃO DE ARQUIVO ###
    # Chama a interface gráfica para o usuário escolher a planilha
    caminho_planilha = selecionar_arquivo_planilha()
    
    # Se o usuário não selecionar um arquivo, encerra o script
    if not caminho_planilha:
        print("\nNenhum arquivo selecionado. Encerrando o programa.")
        return

    print(f"Arquivo selecionado: {caminho_planilha}")
    time.sleep(2) # Pequena pausa para o usuário ler o caminho
    limpar_terminal()

    print("--- INICIANDO AUTOMAÇÃO ATLAS ELETRODOMÉSTICOS ---")
    
    manager = SeleniumManager(headless=True)
    driver = manager.driver
    
    try:
        login_bem_sucedido = fazer_login(driver)
        
        if login_bem_sucedido:
            # Passa o caminho do arquivo para a função de leitura
            dados_a_pesquisar = obter_dados_para_pesquisa(caminho_planilha)
            
            if dados_a_pesquisar:
                resultados_finais = realizar_pesquisas(driver, dados_a_pesquisar)
                
                # Passa os resultados e o caminho para a função de salvar
                salvar_dados_pesquisados(resultados_finais, caminho_planilha)

            print("\nAutomação concluída com sucesso!")
            time.sleep(3)
        else:
            print("\nO login falhou. O script não pode continuar e será encerrado.")
            time.sleep(3)

    except Exception as e:
        print(f"Ocorreu um erro inesperado na automação principal: {e}")
    finally:
        manager.close_driver()

if __name__ == "__main__":
    limpar_terminal()
    iniciar_automacao()