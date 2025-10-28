# Importa as bibliotecas necessárias
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


class SeleniumManager:
    """
    Uma classe para gerenciar a instância do Selenium WebDriver usando um driver local.
    """

    # A função __init__ agora aceita o log_callback da interface
    def __init__(self, headless: bool = False, log_callback=print):
        """
        Inicializa o WebDriver do Chrome com as opções especificadas.
        """
        # Armazena a função de log para ser usada em outros métodos
        self.log_callback = log_callback

        chrome_options = Options()

        # Opções que já estavam corretas
        chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--log-level=3')

        if headless:
            chrome_options.add_argument("--headless")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/536.36")

        # =================================================================
        # ### ALTERAÇÃO PRINCIPAL ###
        # Usa o caminho local para o chromedriver.exe que você colocou na pasta 'components'.
        # =================================================================
        try:
            self.log_callback(
                "Iniciando WebDriver: Verificando/Baixando o ChromeDriver...")

            # Esta é a linha principal:
            # 1. Detecta a versão do seu Chrome.
            # 2. Baixa o chromedriver.exe compatível, se necessário.
            # 3. Retorna o caminho para o executável baixado.
            driver_path = ChromeDriverManager().install()

            # Usa o caminho retornado pelo webdriver-manager
            service = ChromeService(driver_path)

            self.driver = webdriver.Chrome(
                service=service, options=chrome_options)
            self.log_callback(
                "WebDriver do Chrome (gerenciado automaticamente) inicializado com sucesso.")

        except Exception as e:
            # Atualiza a mensagem de erro para refletir o novo método
            self.log_callback(
                f"!!! ERRO ao inicializar o WebDriver automático: {e}")
            self.log_callback("    Verifique sua conexão com a internet.")
            self.log_callback(
                "    Certifique-se de que o Chrome está instalado e que o 'webdriver-manager' tem permissão para baixar arquivos.")
            self.driver = None  # Garante que o driver é None se falhar}

    def close_driver(self):
        """
        Fecha o navegador e encerra a sessão do WebDriver de forma segura.
        """
        if self.driver:
            self.driver.quit()
            # Usa o log_callback aqui também para consistência
            self.log_callback("Sessão do WebDriver encerrada.")
