import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import threading
import os
from PIL import Image
import pandas as pd

# Importa os dois "core" de automação
from automacao_core import iniciar_automacao
from automacao_pecas_core import iniciar_automacao_pecas

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- TEMA E CONFIGURAÇÃO DA JANELA ---
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Assistente de Automação Atlas")
        self.geometry("800x700") # Aumentei um pouco a altura
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1) # O Log agora está na linha 1

        # --- Variáveis de Estado ---
        self.caminho_planilha_atlas = ""
        self.caminho_planilha_pecas = ""
        self.template_filename_atlas = "dados_pesquisa_serie.xlsx"
        self.template_filename_pecas = "dados_pesquisa_pecas.xlsx"
        
        self.cancel_event = threading.Event()
        
        # --- Carregar Ícones ---
        try:
            self.icon_folder = ctk.CTkImage(Image.open("icons/folder.png"), size=(20, 20))
            self.icon_play = ctk.CTkImage(Image.open("icons/play.png"), size=(20, 20))
            self.icon_cancel = ctk.CTkImage(Image.open("icons/cancel.png"), size=(20, 20))
        except FileNotFoundError:
            self.icon_folder, self.icon_play, self.icon_cancel = None, None, None
            print("Aviso: Arquivos de ícone não encontrados na pasta 'icons'.")

        # --- PAINEL DE NAVEGAÇÃO (Esquerda) ---
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, rowspan=2, sticky="nsew") # rowspan=2
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  Automações", font=ctk.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Botão 1
        self.btn_nav_pesquisa_atlas = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, text="Coleta de Modelo por Série",
                                                 fg_color="transparent", text_color=("gray10", "gray90"), anchor="w",
                                                 command=self.frame_pesquisa_atlas_event)
        self.btn_nav_pesquisa_atlas.grid(row=1, column=0, sticky="ew")

        # Botão 2 (Novo)
        self.btn_nav_pesquisa_pecas = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, text="Coleta de Preços por Peça",
                                                 fg_color="transparent", text_color=("gray10", "gray90"), anchor="w",
                                                 command=self.frame_pesquisa_pecas_event)
        self.btn_nav_pesquisa_pecas.grid(row=2, column=0, sticky="ew")


        # --- FRAME PRINCIPAL (Direita - Contêiner para os painéis de automação) ---
        self.main_automation_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_automation_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_automation_frame.grid_columnconfigure(0, weight=1)

        # --- Painel de Automação 1 (ATLAS) ---
        self.frame_atlas = ctk.CTkFrame(self.main_automation_frame, fg_color="transparent")
        self.frame_atlas.grid(row=0, column=0, sticky="nsew")
        self.criar_frame_pesquisa_atlas(self.frame_atlas)

        # --- Painel de Automação 2 (PEÇAS) ---
        self.frame_pecas = ctk.CTkFrame(self.main_automation_frame, fg_color="transparent")
        self.frame_pecas.grid(row=0, column=0, sticky="nsew")
        self.criar_frame_pesquisa_pecas(self.frame_pecas)
        

        # --- FRAME DE LOG (Direita, Embaixo - Compartilhado) ---
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=(0, 20))
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(1, weight=1)
        
        self.log_label = ctk.CTkLabel(self.log_frame, text="Log de Execução", font=ctk.CTkFont(size=16, weight="bold"))
        self.log_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.log_textbox = ctk.CTkTextbox(self.log_frame, state="disabled", wrap="word", corner_radius=0)
        self.log_textbox.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="nsew")
        
        # --- Estado Inicial ---
        self.frame_pesquisa_atlas_event() # Mostra o primeiro frame por padrão

    # --- Funções de Navegação ---
    def select_frame_by_name(self, name):
        """Ativa o botão do menu lateral e mostra o frame correspondente."""
        # Define a cor dos botões
        self.btn_nav_pesquisa_atlas.configure(fg_color=self.btn_nav_pesquisa_atlas.cget("hover_color") if name == "atlas" else "transparent")
        self.btn_nav_pesquisa_pecas.configure(fg_color=self.btn_nav_pesquisa_pecas.cget("hover_color") if name == "pecas" else "transparent")

        # Mostra o frame correto
        if name == "atlas":
            self.frame_atlas.tkraise()
        elif name == "pecas":
            self.frame_pecas.tkraise()

    def frame_pesquisa_atlas_event(self):
        self.select_frame_by_name("atlas")

    def frame_pesquisa_pecas_event(self):
        self.select_frame_by_name("pecas")

    # --- Funções de Geração de UI ---
    
    def criar_frame_pesquisa_atlas(self, parent_frame):
        """Cria os widgets para o painel 'Coleta de Modelo por Série'."""
        
        # --- Frame de Configuração (Atlas) ---
        setup_frame = ctk.CTkFrame(parent_frame)
        setup_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        setup_frame.grid_columnconfigure(1, weight=1) # Coluna 1 expande

        # Título de Identificação
        self.setup_label_atlas = ctk.CTkLabel(setup_frame, text="Coleta de Modelo por Série", font=ctk.CTkFont(size=18, weight="bold"))
        self.setup_label_atlas.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w")
        
        self.setup_label = ctk.CTkLabel(setup_frame, text="1. Configuração", font=ctk.CTkFont(size=16, weight="bold"))
        self.setup_label.grid(row=1, column=0, columnspan=2, padx=15, pady=(5, 5), sticky="w")
        
        self.lbl_arquivo_atlas = ctk.CTkLabel(setup_frame, text="Nenhum arquivo de planilha selecionado.", anchor="w")
        self.lbl_arquivo_atlas.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="ew")
        
        self.btn_selecionar_atlas = ctk.CTkButton(setup_frame, text="Selecionar Planilha", image=self.icon_folder, command=self.selecionar_planilha_atlas_callback)
        self.btn_selecionar_atlas.grid(row=3, column=0, padx=15, pady=(5, 15), sticky="w")
        
        self.btn_modelo_atlas = ctk.CTkButton(setup_frame, text="Gerar Modelo (Área de Trabalho)", command=self.gerar_modelo_atlas_callback)
        self.btn_modelo_atlas.grid(row=3, column=1, padx=(5, 15), pady=(5, 15), sticky="w")

        # --- Frame de Execução (Atlas) ---
        action_frame = ctk.CTkFrame(parent_frame)
        action_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        action_frame.grid_columnconfigure(1, weight=1) 
        
        self.action_label = ctk.CTkLabel(action_frame, text="2. Execução", font=ctk.CTkFont(size=16, weight="bold"))
        self.action_label.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 5), sticky="w")
        
        self.btn_iniciar_atlas = ctk.CTkButton(action_frame, text="Iniciar Coleta de Modelos", image=self.icon_play, command=self.iniciar_processo_atlas_callback, state="disabled")
        self.btn_iniciar_atlas.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="w")
        
        self.btn_cancelar_atlas = ctk.CTkButton(action_frame, text="Cancelar", image=self.icon_cancel, command=self.cancelar_processo_callback, state="disabled", fg_color="#D32F2F", hover_color="#B71C1C")
        self.btn_cancelar_atlas.grid(row=1, column=1, padx=15, pady=(5, 15), sticky="w")
        
        self.progressbar_atlas = ctk.CTkProgressBar(action_frame, mode="indeterminate")

    def criar_frame_pesquisa_pecas(self, parent_frame):
        """Cria os widgets para o painel 'Coleta de Preços por Peça'."""
        
        # --- Frame de Configuração (Peças) ---
        setup_frame = ctk.CTkFrame(parent_frame)
        setup_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        setup_frame.grid_columnconfigure(1, weight=1)

        # Título de Identificação
        self.setup_label_pecas = ctk.CTkLabel(setup_frame, text="Coleta de Preços por Peça", font=ctk.CTkFont(size=18, weight="bold"))
        self.setup_label_pecas.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w")
        
        self.setup_label_p = ctk.CTkLabel(setup_frame, text="1. Configuração", font=ctk.CTkFont(size=16, weight="bold"))
        self.setup_label_p.grid(row=1, column=0, columnspan=2, padx=15, pady=(5, 5), sticky="w")
        
        self.lbl_arquivo_pecas = ctk.CTkLabel(setup_frame, text="Nenhum arquivo de planilha selecionado.", anchor="w")
        self.lbl_arquivo_pecas.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="ew")
        
        self.btn_selecionar_pecas = ctk.CTkButton(setup_frame, text="Selecionar Planilha", image=self.icon_folder, command=self.selecionar_planilha_pecas_callback)
        self.btn_selecionar_pecas.grid(row=3, column=0, padx=15, pady=(5, 15), sticky="w")
        
        self.btn_modelo_pecas = ctk.CTkButton(setup_frame, text="Gerar Modelo (Área de Trabalho)", command=self.gerar_modelo_pecas_callback)
        self.btn_modelo_pecas.grid(row=3, column=1, padx=(5, 15), pady=(5, 15), sticky="w")

        # --- Frame de Execução (Peças) ---
        action_frame = ctk.CTkFrame(parent_frame)
        action_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        action_frame.grid_columnconfigure(1, weight=1)
        
        self.action_label_p = ctk.CTkLabel(action_frame, text="2. Execução", font=ctk.CTkFont(size=16, weight="bold"))
        self.action_label_p.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 5), sticky="w")
        
        self.btn_iniciar_pecas = ctk.CTkButton(action_frame, text="Iniciar Coleta de Preços", image=self.icon_play, command=self.iniciar_processo_pecas_callback, state="disabled")
        self.btn_iniciar_pecas.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="w")
        
        self.btn_cancelar_pecas = ctk.CTkButton(action_frame, text="Cancelar", image=self.icon_cancel, command=self.cancelar_processo_callback, state="disabled", fg_color="#D32F2F", hover_color="#B71C1C")
        self.btn_cancelar_pecas.grid(row=1, column=1, padx=15, pady=(5, 15), sticky="w")
        
        self.progressbar_pecas = ctk.CTkProgressBar(action_frame, mode="indeterminate")

    # --- Funções de Callback (Genéricas) ---
    
    def log_message(self, message):
        """Adiciona uma mensagem ao textbox de log compartilhado."""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert(tk.END, message + "\n")
        self.log_textbox.see(tk.END)
        self.log_textbox.configure(state="disabled")

    def cancelar_processo_callback(self):
        """Ativa o evento de cancelamento e desativa os botões."""
        self.log_message("\n!!! Sinal de cancelamento enviado. Aguardando a tarefa atual ser concluída... !!!")
        self.cancel_event.set() 
        self.btn_cancelar_atlas.configure(state="disabled")
        self.btn_cancelar_pecas.configure(state="disabled")

    def set_buttons_state(self, state: str):
        """Ativa ou desativa todos os botões de interação."""
        self.btn_selecionar_atlas.configure(state=state)
        self.btn_modelo_atlas.configure(state=state)
        self.btn_iniciar_atlas.configure(state=state if state == "normal" and self.caminho_planilha_atlas else "disabled")
        
        self.btn_selecionar_pecas.configure(state=state)
        self.btn_modelo_pecas.configure(state=state)
        self.btn_iniciar_pecas.configure(state=state if state == "normal" and self.caminho_planilha_pecas else "disabled")
        
        # Botões de navegação
        self.btn_nav_pesquisa_atlas.configure(state=state)
        self.btn_nav_pesquisa_pecas.configure(state=state)
        
        # Botões de cancelar são tratados separadamente
        if state == "disabled":
            self.btn_cancelar_atlas.configure(state="normal")
            self.btn_cancelar_pecas.configure(state="normal")
        else:
            self.btn_cancelar_atlas.configure(state="disabled")
            self.btn_cancelar_pecas.configure(state="disabled")

    def gerar_modelo_desktop(self, filename: str, sheet_name: str, columns: list):
        """Função genérica para criar arquivos modelo na Área de Trabalho."""
        try:
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            caminho_completo_arquivo = os.path.join(desktop_path, filename)

            if not os.path.exists(caminho_completo_arquivo):
                self.log_message(f"Criando arquivo modelo em: {caminho_completo_arquivo}...")
                df_modelo = pd.DataFrame(columns=columns)
                df_modelo.to_excel(caminho_completo_arquivo, sheet_name=sheet_name, index=False)
                self.log_message(f"Arquivo modelo '{filename}' salvo na sua Área de Trabalho.")
            else:
                self.log_message(f"O arquivo modelo '{filename}' já existe na sua Área de Trabalho.")
        except Exception as e:
            self.log_message(f"!!! ERRO ao salvar o arquivo modelo '{filename}': {e}")

    # --- Callbacks Específicos (ATLAS - Modelo por Série) ---
    
    def selecionar_planilha_atlas_callback(self):
        caminho = filedialog.askopenfilename(title="Selecione a planilha (Série)", filetypes=[("Planilhas Excel", "*.xlsx")])
        if caminho:
            self.caminho_planilha_atlas = caminho
            self.lbl_arquivo_atlas.configure(text=f"{os.path.basename(caminho)}")
            self.btn_iniciar_atlas.configure(state="normal")
            self.log_message(f"Planilha (Série) selecionada: {self.caminho_planilha_atlas}")

    def gerar_modelo_atlas_callback(self):
        self.gerar_modelo_desktop(self.template_filename_atlas, "Dados", ["Serie", "Modelo"])

    def iniciar_processo_atlas_callback(self):
        if not self.caminho_planilha_atlas:
            self.log_message("ERRO: Por favor, selecione uma planilha (Série) primeiro.")
            return

        self.cancel_event.clear()
        self.set_buttons_state("disabled")
        
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", tk.END)
        self.log_textbox.configure(state="disabled")

        self.progressbar_atlas.grid(row=2, column=0, columnspan=2, padx=15, pady=(5, 15), sticky="ew")
        self.progressbar_atlas.start()

        threading.Thread(target=self.run_automation_atlas_thread).start()
        
    def run_automation_atlas_thread(self):
        try:
            iniciar_automacao(self.caminho_planilha_atlas, self.log_message, self.cancel_event)
        except Exception as e:
            self.log_message(f"ERRO CRÍTICO (ATLAS): {e}")
        finally:
            self.progressbar_atlas.stop()
            self.progressbar_atlas.grid_forget()
            self.set_buttons_state("normal")
            self.log_message("\n--- Processo (Série) finalizado. ---")

    # --- Callbacks Específicos (PEÇAS - Preço por Peça) ---

    def selecionar_planilha_pecas_callback(self):
        caminho = filedialog.askopenfilename(title="Selecione a planilha (Peças)", filetypes=[("Planilhas Excel", "*.xlsx")])
        if caminho:
            self.caminho_planilha_pecas = caminho
            self.lbl_arquivo_pecas.configure(text=f"{os.path.basename(caminho)}")
            self.btn_iniciar_pecas.configure(state="normal")
            self.log_message(f"Planilha (Peças) selecionada: {self.caminho_planilha_pecas}")

    def gerar_modelo_pecas_callback(self):
        self.gerar_modelo_desktop(self.template_filename_pecas, "Dados_Pecas", ["Codigo", "Descricao", "Valor"])

    def iniciar_processo_pecas_callback(self):
        if not self.caminho_planilha_pecas:
            self.log_message("ERRO: Por favor, selecione uma planilha (Peças) primeiro.")
            return

        self.cancel_event.clear()
        self.set_buttons_state("disabled")

        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", tk.END)
        self.log_textbox.configure(state="disabled")

        self.progressbar_pecas.grid(row=2, column=0, columnspan=2, padx=15, pady=(5, 15), sticky="ew")
        self.progressbar_pecas.start()

        threading.Thread(target=self.run_automation_pecas_thread).start()
        
    def run_automation_pecas_thread(self):
        try:
            iniciar_automacao_pecas(self.caminho_planilha_pecas, self.log_message, self.cancel_event)
        except Exception as e:
            self.log_message(f"ERRO CRÍTICO (PEÇAS): {e}")
        finally:
            self.progressbar_pecas.stop()
            self.progressbar_pecas.grid_forget()
            self.set_buttons_state("normal")
            self.log_message("\n--- Processo (Peças) finalizado. ---")

if __name__ == "__main__":
    app = App()
    app.mainloop()