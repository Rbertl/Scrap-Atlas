from config_selenium import SeleniumManager
from login.login import fazer_login # Importa a função do nosso módulo de login
import time

def iniciar_automacao():
    """
    Função principal que orquestra todo o processo de automação.
    """
    # Cria uma instância do nosso gerenciador do Selenium
    manager = SeleniumManager(headless=False)
    # Pega o driver para ser usado nas funções
    driver = manager.driver
    
    try:
        # ETAPA 1: Executar o processo de login
        # Passamos o driver para a função de login
        login_bem_sucedido = fazer_login(driver)
        
        # ETAPA 2: Prosseguir com outras tarefas apenas se o login funcionar
        if login_bem_sucedido:
            print("\nContinuando com as tarefas principais após o login...")
            
            # Daqui para frente, você pode adicionar a lógica principal do seu scraping.
            # O driver já está logado e pronto para ser usado.
            
            input('')
            time.sleep(10)
            
        else:
            print("\nO login falhou. O script não pode continuar e será encerrado.")

    except Exception as e:
        # Captura e imprime qualquer exceção que possa ocorrer
        print(f"Ocorreu um erro inesperado na automação principal: {e}")
    finally:
        # Garante que o navegador seja fechado ao final, mesmo se ocorrerem erros.
        manager.close_driver()

# Ponto de entrada do script principal
if __name__ == "__main__":
    iniciar_automacao()