import pandas as pd
import os

def obter_dados_para_pesquisa(caminho_do_arquivo: str, log_callback=print):
    """
    Lê a coluna 'Serie' de um arquivo Excel, garantindo que seja lida como texto.
    
    :param caminho_do_arquivo: O caminho completo para o arquivo Excel selecionado pelo usuário.
    :param log_callback: A função para enviar mensagens de log para a interface.
    """
    log_callback("Extraindo dados do arquivo Excel para a pesquisa...")
    try:
        df = pd.read_excel(
            caminho_do_arquivo, 
            sheet_name='Dados', 
            usecols='A', 
            dtype={'Serie': str}
        )
        df.dropna(inplace=True)
        dados = df['Serie'].tolist()
        
        log_callback(f"{len(dados)} itens encontrados para pesquisar.")
        return dados
        
    except FileNotFoundError:
        log_callback(f"!!! ERRO: Arquivo '{caminho_do_arquivo}' não encontrado!")
        log_callback("    Certifique-se de que o arquivo Excel existe e tem o nome correto.")
        return []
    except Exception as e:
        log_callback(f"!!! Ocorreu um erro ao ler o arquivo Excel: {e}")
        return []

def salvar_dados_pesquisados(resultados: list, caminho_do_arquivo: str, log_callback=print):
    """
    Salva os resultados da pesquisa de volta no arquivo Excel.
    
    :param resultados: A lista de dicionários com os resultados.
    :param caminho_do_arquivo: O caminho do arquivo onde os dados serão salvos.
    :param log_callback: A função para enviar mensagens de log para a interface.
    """
    if not resultados:
        log_callback("Nenhum resultado para salvar.")
        return
        
    log_callback("\nSalvando resultados no arquivo Excel...")
    try:
        df = pd.read_excel(
            caminho_do_arquivo, 
            sheet_name='Dados',
            dtype={'Serie': str}
        )

        for resultado in resultados:
            serie = resultado['Serie']
            modelo = resultado['Modelo']
            df.loc[df['Serie'] == serie, 'Modelo'] = modelo

        df.to_excel(caminho_do_arquivo, sheet_name='Dados', index=False)
        log_callback(">>> Resultados salvos com sucesso!")

    except Exception as e:
        log_callback(f"!!! Ocorreu um erro ao salvar os dados no Excel: {e}")