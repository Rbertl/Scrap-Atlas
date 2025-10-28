import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import threading
import os
from PIL import Image

# --- Imports Adicionados (Pandas para criar o Excel) ---
import pandas as pd
# -------------------------

from automacao_core import iniciar_automacao

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- TEMA E CONFIGURAÇÃO DA JANELA ---
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Assistente de Automação Atlas")
        self.geometry("800x650")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.caminho_planilha = ""
        self.cancel_event = threading.Event()
        
        # --- Nome do arquivo modelo ---
        self.template_filename = "dados_pesquisa.xlsx"
        
        # ... (código para carregar ícones) ...
        try:
            self.icon_folder = ctk.CTkImage(Image.open("icons/folder.png"), size=(20, 20))
            self.icon_play = ctk.CTkImage(Image.open("icons/play.png"), size=(20, 20))
            self.icon_cancel = ctk.CTkImage(Image.open("icons/cancel.png"), size=(20, 20))
        except FileNotFoundError:
            self.icon_folder, self.icon_play, self.icon_cancel = None, None, None
            print("Aviso: Arquivos de ícone não encontrados na pasta 'icons'.")

        # --- PAINEL DE NAVEGAÇÃO ---
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  Automações", font=ctk.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        self.btn_pesquisa_atlas = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, text="Coleta de Modelo por Série", command=self.frame_pesquisa_atlas_button_event)
        self.btn_pesquisa_atlas.grid(row=1, column=0, sticky="ew")

        # --- FRAME PRINCIPAL ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # --- Frame de Configuração (Modificado) ---
        self.setup_frame = ctk.CTkFrame(self.main_frame)
        self.setup_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.setup_label = ctk.CTkLabel(self.setup_frame, text="1. Configuração", font=ctk.CTkFont(size=16, weight="bold"))
        self.setup_label.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 5), sticky="w") 
        
        self.lbl_arquivo = ctk.CTkLabel(self.setup_frame, text="Nenhum arquivo de planilha selecionado.", anchor="w")
        self.lbl_arquivo.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="ew")
        
        self.btn_selecionar = ctk.CTkButton(self.setup_frame, text="Selecionar Planilha", image=self.icon_folder, command=self.selecionar_planilha_callback)
        self.btn_selecionar.grid(row=2, column=0, padx=15, pady=(5, 15), sticky="w")

        # --- BOTÃO MODELO (Modificado) ---
        self.btn_modelo = ctk.CTkButton(self.setup_frame, 
                                        text="Gerar Modelo (Área de Trabalho)", 
                                        command=self.gerar_modelo_desktop_callback)
        self.btn_modelo.grid(row=2, column=1, padx=(5, 15), pady=(5, 15), sticky="w")
        # -------------------------

        # --- Frame de Execução ---
        self.action_frame = ctk.CTkFrame(self.main_frame)
        self.action_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.action_frame.grid_columnconfigure(1, weight=1) 
        
        self.action_label = ctk.CTkLabel(self.action_frame, text="2. Execução", font=ctk.CTkFont(size=16, weight="bold"))
        self.action_label.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 5), sticky="w")

        self.btn_iniciar = ctk.CTkButton(self.action_frame, text="Iniciar Processo de Coleta", image=self.icon_play, command=self.iniciar_processo_callback, state="disabled")
        self.btn_iniciar.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="w")
        
        self.btn_cancelar = ctk.CTkButton(self.action_frame, text="Cancelar", image=self.icon_cancel, command=self.cancelar_processo_callback, state="disabled", fg_color="#D32F2F", hover_color="#B71C1C")
        self.btn_cancelar.grid(row=1, column=1, padx=15, pady=(5, 15), sticky="w")
        
        self.progressbar = ctk.CTkProgressBar(self.action_frame, mode="indeterminate")
        
        # --- Frame de Log ---
        self.log_frame = ctk.CTkFrame(self.main_frame)
        self.log_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(1, weight=1)
        self.log_label = ctk.CTkLabel(self.log_frame, text="Log de Execução", font=ctk.CTkFont(size=16, weight="bold"))
        self.log_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        self.log_textbox = ctk.CTkTextbox(self.log_frame, state="disabled", wrap="word", corner_radius=0)
        self.log_textbox.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="nsew")
        
        self.frame_pesquisa_atlas_button_event()

    def selecionar_planilha_callback(self):
        tipos_de_arquivo = [("Planilhas Excel", "*.xlsx"), ("Todos os arquivos", "*.*")]
        caminho = filedialog.askopenfilename(title="Selecione a planilha", filetypes=tipos_de_arquivo)
        if caminho:
            self.caminho_planilha = caminho
            self.lbl_arquivo.configure(text=f"{os.path.basename(caminho)}")
            self.btn_iniciar.configure(state="normal")
            self.log_message(f"Planilha selecionada: {self.caminho_planilha}")
    
    def cancelar_processo_callback(self):
        self.log_message("\n!!! Sinal de cancelamento enviado. Aguardando a tarefa atual ser concluída... !!!")
        self.cancel_event.set() 
        self.btn_cancelar.configure(state="disabled")

    # ### FUNÇÃO DO BOTÃO MODELO (Atualizada) ###
    def gerar_modelo_desktop_callback(self):
        """
        Cria um arquivo modelo na Área de Trabalho do usuário, se ainda não existir.
        """
        try:
            # 1. Encontra a Área de Trabalho de forma universal
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            
            # 2. Define o caminho completo do arquivo
            caminho_completo_arquivo = os.path.join(desktop_path, self.template_filename)

            # 3. Verifica se o arquivo já existe
            if not os.path.exists(caminho_completo_arquivo):
                self.log_message(f"Criando arquivo modelo em: {caminho_completo_arquivo}...")
                
                # 4. Cria o DataFrame e salva no formato correto
                df_modelo = pd.DataFrame(columns=['Serie', 'Modelo'])
                df_modelo.to_excel(caminho_completo_arquivo, sheet_name='Dados', index=False)
                
                self.log_message(f"Arquivo modelo '{self.template_filename}' salvo na sua Área de Trabalho.")
            else:
                # 5. Se já existe, apenas avisa o usuário
                self.log_message(f"O arquivo modelo '{self.template_filename}' já existe na sua Área de Trabalho.")
                self.log_message(f"Caminho: {caminho_completo_arquivo}")

        except Exception as e:
            self.log_message(f"!!! ERRO ao salvar o arquivo modelo: {e}")
            self.log_message("    Verifique se o script tem permissão para escrever na Área de Trabalho.")

    def iniciar_processo_callback(self):
        if not self.caminho_planilha:
            self.log_message("ERRO: Por favor, selecione uma planilha primeiro.")
            return

        self.cancel_event.clear() 
        self.btn_iniciar.configure(state="disabled")
        self.btn_selecionar.configure(state="disabled")
        self.btn_cancelar.configure(state="normal")
        self.btn_modelo.configure(state="disabled") # --- Desativa o botão modelo ---
        
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", tk.END)
        self.log_textbox.configure(state="disabled")

        self.progressbar.grid(row=2, column=0, columnspan=2, padx=15, pady=(5, 15), sticky="ew")
        self.progressbar.start()

        automation_thread = threading.Thread(target=self.run_automation_thread)
        automation_thread.start()
        
    def run_automation_thread(self):
        try:
            iniciar_automacao(self.caminho_planilha, self.log_message, self.cancel_event)
        except Exception as e:
            self.log_message(f"ERRO CRÍTICO NA AUTOMAÇÃO: {e}")
        finally:
            self.progressbar.stop()
            self.progressbar.grid_forget()
            self.btn_iniciar.configure(state="normal")
            self.btn_selecionar.configure(state="normal")
            self.btn_cancelar.configure(state="disabled") 
            self.btn_modelo.configure(state="normal") # --- Reativa o botão modelo ---
            self.log_message("\n--- Processo finalizado. ---")
            
    def log_message(self, message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert(tk.END, message + "\n")
        self.log_textbox.see(tk.END)
        self.log_textbox.configure(state="disabled")

    def frame_pesquisa_atlas_button_event(self):
        self.main_frame.grid(row=0, column=1, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()