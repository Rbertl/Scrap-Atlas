import PyInstaller.__main__
import os

# Nome do seu aplicativo e do script principal
nome_do_app = "AssistenteAtlas"
script_principal = "app_gui.py"
icone_do_app = "app_icon.ico"

# --- Configurações do PyInstaller ---
opcoes = [
    '--name=%s' % nome_do_app,
    '--onefile', # Cria um único arquivo .exe
    '--windowed', # Remove o console do terminal ao executar o .exe
    '--clean', # Limpa os arquivos temporários antes de construir
    
    # Adiciona a pasta de componentes (com o chromedriver.exe) ao pacote
    '--add-data=%s' % 'components;components',
    
    # Adiciona a pasta de ícones (com os .png) ao pacote
    '--add-data=%s' % 'icons;icons',
]

# Adiciona o ícone ao .exe, se o arquivo existir
if os.path.exists(icone_do_app):
    opcoes.append('--icon=%s' % icone_do_app)

# Junta as opções com o nome do script principal
comando_final = opcoes + [script_principal]


if __name__ == '__main__':
    print("Iniciando a geração do executável com PyInstaller...")
    print(f"Comando: {' '.join(comando_final)}")
    
    # Executa o PyInstaller com as configurações definidas
    PyInstaller.__main__.run(comando_final)
    
    print("\nProcesso de geração do .exe concluído!")
    print(f"Seu aplicativo '{nome_do_app}.exe' está na pasta 'dist'.")