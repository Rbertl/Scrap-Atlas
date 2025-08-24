import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# A linha abaixo só é necessária se você executar este arquivo de login diretamente para teste
if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config_selenium import SeleniumManager

def fazer_login(driver: WebDriver):
    """
    Realiza o login no site usando um driver do Selenium já inicializado.
    
    :param driver: A instância do WebDriver a ser usada.
    :return: True se o login for bem-sucedido, False caso contrário.
    """
    try:
        login_url = "https://atlaseletro.my.site.com/NewAuthorizedCommunity/s/login/"
        print(f"Acessando a URL de login: {login_url}")
        driver.get(login_url)

        wait = WebDriverWait(driver, 20)

        print("Aguardando campo de login...")
        campo_login = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sfdc_username_container"]//input')))
        campo_login.send_keys("11300964000171@atlas.ind.br")
        print("Campo de login preenchido.")

        campo_senha = driver.find_element(By.XPATH, '//*[@id="sfdc_password_container"]//input')
        campo_senha.send_keys("Maq@123Bh")
        print("Campo de senha preenchido.")

        print("Procurando o botão de login...")
        botao_login = driver.find_element(By.XPATH, '//*[@id="centerPanel"]/div/div[2]/div/div[2]/div/div[3]/button')
        botao_login.click()
        print("Botão de login pressionado.")

        # #######################################################################
        # ### ALTERAÇÃO PRINCIPAL AQUI ###
        # Agora esperamos pela mensagem de boas-vindas que você indicou.
        # #######################################################################
        print("Aguardando carregamento da página principal...")
        
        # Seletor que procura por QUALQUER elemento (*) que contenha o texto de boas-vindas.
        seletor_bem_vindo = (By.XPATH, "//*[contains(text(), 'Seja Bem-vindo a nova Comunidade da ATLAS ELETRODOMÉSTICOS!')]")
        
        # O script vai pausar aqui até que o elemento com o texto esteja VISÍVEL na tela.
        wait.until(EC.visibility_of_element_located(seletor_bem_vindo))
        
        print("\nLogin realizado com sucesso e página principal totalmente carregada!")
        return True

    except Exception as e:
        print(f"\nOcorreu um erro durante o processo de login: {e}")
        return False

# Ponto de entrada para testar o script de login de forma isolada
if __name__ == "__main__":
    print("--- Executando o script de login de forma isolada para teste ---")
    manager = SeleniumManager(headless=False)
    
    sucesso = fazer_login(manager.driver)

    if sucesso:
        print(f"Teste de login bem-sucedido. URL final: {manager.driver.current_url}")
        import time
        time.sleep(5) # Pausa para ver o resultado
    else:
        print("Teste de login falhou.")
    
    manager.close_driver()