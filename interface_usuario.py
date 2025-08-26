import tkinter as tk
from tkinter import filedialog, messagebox

def selecionar_arquivo_planilha():
    """
    Exibe uma janela de instruções e, em seguida, uma janela para o usuário
    selecionar um arquivo de planilha. A janela de seleção fica no topo.
    
    :return: O caminho completo do arquivo selecionado, ou None se o usuário cancelar.
    """
    # Inicializa o Tkinter e esconde a janela principal
    root = tk.Tk()
    root.withdraw()
    
    # Faz com que as janelas de diálogo apareçam no topo de todas as outras
    root.attributes('-topmost', True)

    # Mensagem de instruções para o usuário
    instrucoes = (
        "ORGANIZAÇÃO DA PLANILHA\n\n"
        "Para que o script funcione corretamente, sua planilha deve seguir este formato:\n\n"
        "1. A aba (planilha) principal deve se chamar exatamente 'Dados'.\n\n"
        "2. A Coluna A deve conter os números de série, com o cabeçalho 'Serie' na célula A1.\n\n"
        "3. A Coluna B deve ter o cabeçalho 'Modelo' na célula B1. Ela será preenchida automaticamente.\n\n"
        "Clique em 'OK' para selecionar o arquivo."
    )
    
    # Exibe a caixa de mensagem com as instruções
    messagebox.showinfo("Instruções de Uso", instrucoes)

    # Tipos de arquivo permitidos na janela de seleção
    tipos_de_arquivo = [
        ("Planilhas Excel", "*.xlsx"),
        ("Planilhas Excel (Antigo)", "*.xls"),
        ("Planilhas OpenDocument", "*.ods"),
        ("Arquivos CSV", "*.csv"),
        ("Todos os arquivos", "*.*")
    ]
    
    # Abre a janela para selecionar o arquivo e captura o caminho
    caminho_do_arquivo = filedialog.askopenfilename(
        title="Selecione a planilha de dados",
        filetypes=tipos_de_arquivo
    )

    # Garante que a janela principal seja destruída
    root.destroy()
    
    if caminho_do_arquivo:
        return caminho_do_arquivo
    else:
        # Retorna None se o usuário fechar a janela sem selecionar
        return None