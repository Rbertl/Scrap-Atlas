# Importa as bibliotecas necessárias do Selenium e do webdriver-manager
# CORREÇÃO: Importa o webdriver da biblioteca selenium, não do próprio arquivo.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


class SeleniumManager:
    """
    Uma classe para gerenciar a instância do Selenium WebDriver.
    Isso centraliza a configuração e facilita a reutilização em diferentes partes do projeto.
    """

    def __init__(self, headless: bool = False):
        """
        Inicializa o WebDriver do Chrome com as opções especificadas.

        :param headless: Se True, o navegador será executado em modo headless (sem interface gráfica).
                         O padrão é False para que você possa ver o navegador em ação durante o desenvolvimento.
        """
        # Configura as opções do Chrome para uma experiência de scraping mais estável
        chrome_options = Options()

        # ADICIONADO: Remove o aviso "O Chrome está sendo controlado por um software de teste automatizado"
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        if headless:
            chrome_options.add_argument("--headless")

        # Necessário para rodar em alguns ambientes (ex: Docker)
        chrome_options.add_argument("--no-sandbox")
        # Evita problemas de memória compartilhada
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Desabilita a aceleração por hardware, útil em modo headless
        chrome_options.add_argument("--disable-gpu")
         # ADICIONE ESTA LINHA para reduzir a quantidade de logs no console
        chrome_options.add_argument("--log-level=3") 
        # Inicia o navegador maximizado
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        # O webdriver-manager baixa e gerencia o chromedriver automaticamente
        service = ChromeService('components/chromedriver.exe')

        # Inicializa o driver do Chrome. O driver fica acessível através de self.driver
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        print("WebDriver do Chrome inicializado.")

    def close_driver(self):
        """
        Fecha o navegador e encerra a sessão do WebDriver de forma segura.
        """
        if self.driver:
            self.driver.quit()
            print("Sessão do WebDriver encerrada.")
