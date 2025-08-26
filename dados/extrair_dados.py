import pandas as pd
import os

# A constante CAMINHO_ARQUIVO foi removida daqui.

def obter_dados_para_pesquisa(caminho_do_arquivo: str):
    """
    Lê a coluna 'Serie' de um arquivo Excel, garantindo que seja lida como texto.
    
    :param caminho_do_arquivo: O caminho completo para o arquivo Excel selecionado pelo usuário.
    """
    print("Extraindo dados do arquivo Excel para a pesquisa...")
    try:
        df = pd.read_excel(
            caminho_do_arquivo, 
            sheet_name='Dados', 
            usecols='A', 
            dtype={'Serie': str}
        )
        df.dropna(inplace=True)
        dados = df['Serie'].tolist()
        
        print(f"{len(dados)} itens encontrados para pesquisar.")
        return dados
        
    except FileNotFoundError:
        print(f"!!! ERRO: Arquivo '{caminho_do_arquivo}' não encontrado!")
        return []
    except Exception as e:
        print(f"!!! Ocorreu um erro ao ler o arquivo Excel: {e}")
        return []

def salvar_dados_pesquisados(resultados: list, caminho_do_arquivo: str):
    """
    Salva os resultados da pesquisa de volta no arquivo Excel.
    
    :param resultados: A lista de dicionários com os resultados.
    :param caminho_do_arquivo: O caminho do arquivo onde os dados serão salvos.
    """
    if not resultados:
        print("Nenhum resultado para salvar.")
        return
        
    print("\nSalvando resultados no arquivo Excel...")
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
        print(">>> Resultados salvos com sucesso!")

    except Exception as e:
        print(f"!!! Ocorreu um erro ao salvar os dados no Excel: {e}")