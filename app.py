import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Importa a função do serviço (certifique-se de que o arquivo corrigir_h020serv.py está na mesma pasta ou no módulo correto)
from corrigir_h020serv import corrigir_h020_faltante

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Corretor EFD - H020 Faltante")
        self.geometry("650x450")
        ctk.set_appearance_mode("System") 
        ctk.set_default_color_theme("blue")

        # Variáveis de Caminho
        self.caminho_entrada = ctk.StringVar()
        self.caminho_saida = ctk.StringVar()

        self._build_ui()

    def _build_ui(self):
        # Título
        lbl_titulo = ctk.CTkLabel(
            self, text="Corrigir H020 Faltante no EFD", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        lbl_titulo.pack(pady=(20, 10), padx=20, anchor="w")

        # Descrição
        lbl_desc = ctk.CTkLabel(
            self, 
            text="Gera automaticamente o registro H020 com base no valor do H010 e \nreplica o totalizador |9900|H020| no final do arquivo.",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            justify="left"
        )
        lbl_desc.pack(pady=(0, 20), padx=20, anchor="w")

        # Frame de Entrada
        frame_in = ctk.CTkFrame(self)
        frame_in.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(frame_in, text="Arquivo de Entrada (TXT):").pack(anchor="w", padx=10, pady=(10, 0))
        
        box_in = ctk.CTkFrame(frame_in, fg_color="transparent")
        box_in.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkEntry(box_in, textvariable=self.caminho_entrada, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(box_in, text="Procurar", width=100, command=self._selecionar_entrada).pack(side="left")

        # Frame de Saída
        frame_out = ctk.CTkFrame(self)
        frame_out.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(frame_out, text="Arquivo Corrigido (Saída):").pack(anchor="w", padx=10, pady=(10, 0))
        
        box_out = ctk.CTkFrame(frame_out, fg_color="transparent")
        box_out.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkEntry(box_out, textvariable=self.caminho_saida, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(box_out, text="Salvar Como", width=100, command=self._selecionar_saida).pack(side="left")

        # Botão de Ação
        btn_corrigir = ctk.CTkButton(
            self, text="Processar Arquivo", 
            height=40, font=ctk.CTkFont(weight="bold"),
            command=self._processar
        )
        btn_corrigir.pack(fill="x", padx=20, pady=(0, 10))

        # Label de Status
        self.lbl_status = ctk.CTkLabel(self, text="", text_color="green", justify="left")
        self.lbl_status.pack(padx=20, anchor="w")

    def _selecionar_entrada(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o EFD TXT",
            filetypes=[("Arquivo TXT", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            self.caminho_entrada.set(caminho)
            base, ext = os.path.splitext(caminho)
            self.caminho_saida.set(f"{base}_CORRIGIDO{ext}")
            self.lbl_status.configure(text="")

    def _selecionar_saida(self):
        entrada = self.caminho_entrada.get()
        initial = "EFD_CORRIGIDO.TXT"
        if entrada:
            base = os.path.basename(entrada)
            nome, ext = os.path.splitext(base)
            initial = f"{nome}_CORRIGIDO{ext or '.TXT'}"

        caminho = filedialog.asksaveasfilename(
            title="Salvar como",
            defaultextension=".TXT",
            initialfile=initial,
            filetypes=[("Arquivo TXT", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            self.caminho_saida.set(caminho)

    def _processar(self):
        entrada = self.caminho_entrada.get().strip()
        saida = self.caminho_saida.get().strip()

        if not entrada or not saida:
            messagebox.showwarning("Atenção", "Selecione o arquivo de entrada e o local de saída.")
            return

        if entrada == saida:
            messagebox.showwarning("Atenção", "O arquivo de saída deve ter um nome diferente da entrada.")
            return

        try:
            resultado = corrigir_h020_faltante(entrada, saida)
            
            texto_status = (
                f"✅ Concluído!\n"
                f"H010 processados: {resultado['h010_encontrados']} | "
                f"H020 inseridos: {resultado['h020_inseridos']} | "
                f"H020 já existentes: {resultado['h020_existentes']}\n"
                f"Totalizadores do Bloco 9 ajustados."
            )
            self.lbl_status.configure(text=texto_status, text_color="#2ecc71") # Verde CTK

        except Exception as e:
            self.lbl_status.configure(text=f"Erro: {str(e)}", text_color="#e74c3c") # Vermelho CTK

if __name__ == "__main__":
    app = App()
    app.mainloop()