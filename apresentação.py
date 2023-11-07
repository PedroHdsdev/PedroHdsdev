from tkinter import ttk, messagebox
import tkinter as tk
from PIL import Image, ImageTk
import os
import pyodbc

class banco_dado:
    def __init__(self):
            self.conn = self.conexao_banco()
    def conexao_banco(self):
        try:
            server = '34.95.204.149'
            database = 'k2kbancodedados'
            username = 'sqlserver'
            password = 'k2k123'
            driver = '{ODBC Driver 17 for SQL Server}'

            conn = pyodbc.connect(f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}')
            return conn
        except pyodbc.Error as err:
            messagebox.showinfo("erro de conexão",f"Erro ao conectar-se ao mysql:{err}")
            return None
    def fechar_conexao(self):
        if self.conn:
            self.conn.close()
    def chamar_tabela(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                SELECT
                    PRO_NOME AS 'NOME',
                    PRO_DATA_INICIO AS 'DATA INICIO',
                    PRO_DATA_ENTREGA AS 'DATA DE ENTREGA',
                    PRO_DATA_TERMINO AS 'DATA TERMINO',
                    PRO_STATUS AS 'STATUS'
                FROM PROJETO
                ORDER BY PRO_DATA_ENTREGA ASC
                """)
                resultados = cursor.fetchall()
                colunas = [column[0] for column in cursor.description]
                return resultados,colunas
            except pyodbc.Error as err:
                print(f"Erro ao chamar a tabela: {err}")
        return None
class janela_login:
    def __init__(self, master):
        self.master = master
        master.title("K2K MOVELARIA")
        largura_janela = 800
        altura_janela = 400
        largura_tela = master.winfo_screenwidth()
        altura_tela = master.winfo_screenheight()
        x = (largura_tela - largura_janela) // 2
        y = (altura_tela - altura_janela) // 2
        master.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

        master.grid_rowconfigure(4, weight=1)
        master.grid_columnconfigure(2, weight=1)
        master.configure(bg="white")

        frame_login_logo = tk.Frame(master,bg="white")
        frame_login_logo.grid(row=1, column=2)

        image_logo = Image.open("C:\\Users\\pedro\\Documents\\python\\K2KMOVELARIA\\logo.jpg")
        image_logo.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(image_logo)
        self.imagem_login_logo = tk.Label(frame_login_logo, image=photo,bg="white")
        self.imagem_login_logo.photo = photo
        self.imagem_login_logo.grid(row=1, column=2, columnspan=2, pady=10,sticky="n")

        frame_text = tk.Frame(master,bg="white")
        frame_text.grid(row=2, column=2)
        
        tk.Label(frame_text, text="Usuário:",bg="white",font=("cambria",12,"bold")).grid(row=1, column=1,pady=20)
        self.username_entry = tk.Entry(frame_text)
        self.username_entry.grid(row=1, column=2,columnspan=2)

        tk.Label(frame_text, text="Senha:",bg="white",font=("cambria",12,"bold")).grid(row=3, column=1, pady=10)
        self.password_entry = tk.Entry(frame_text, show="*") 
        self.password_entry.grid(row=3, column=2)

        botao_frame = tk.Frame(master,bg="white")
        botao_frame.grid(row=4, column=2,columnspan=2,pady=5)

        self.botao_abrir_menu = tk.Button(botao_frame, text="Entrar",bg="white",font=("cambria",12,"bold"), command=self.abrir_menu)
        self.botao_abrir_menu.grid(row=0, column=2, padx=10)

        self.botao_fechar_login = tk.Button(botao_frame, text="Sair",bg="white",font=("cambria",12,"bold"), command=self.fechar_login)
        self.botao_fechar_login.grid(row=0, column=3, padx=10)
        
    def abrir_menu(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "pedro" and password == "123":
            self.master.withdraw()
            self.janela_projetos = projetos(self.master)  

        elif username == "123" and password == "123":
            self.master.withdraw()
            self.janela_almoxerifado = almoxerifado(self.master)  
        else:
            messagebox.showerror(f"Erro de Login","Usuario ou Senha Invalido !")
    def fechar_login(self):
        self.master.destroy()
class projetos:
    def __init__(self, master):
        self.master = master
        self.projetos = tk.Toplevel(self.master)
        self.projetos.title("K2K PROJETOS")
        largura_janela = 900
        altura_janela = 600
        largura_tela = master.winfo_screenwidth()
        altura_tela = master.winfo_screenheight()
        x = (largura_tela - largura_janela) // 2
        y = (altura_tela - altura_janela) // 2
        self.projetos.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

        self.projetos.grid_rowconfigure(2, weight=1)
        self.projetos.grid_columnconfigure(3, weight=1)
        self.projetos.configure(bg="white")

        frame_pesquisa = tk.Frame(self.projetos,bg="white",relief="solid", borderwidth=1)
        frame_pesquisa.grid(row=0, column=2,sticky="n",pady=15,columnspan=2)
        
        frame_pesquisa1 = tk.Frame(frame_pesquisa,bg="white")
        frame_pesquisa1.grid(row=1, column=3,sticky="e",pady=5)

        frame_menu = tk.Frame(self.projetos,bg="white")
        frame_menu.grid(row=2, column=3,sticky="n",pady=5,columnspan=2)

        frame_tabela = tk.Frame(self.projetos,bg="white",relief="solid", borderwidth=1)
        frame_tabela.grid(row=2, column=2,sticky="n",pady=10,padx=10)

        frame_logo = tk.Frame(self.projetos,bg="white")
        frame_logo.grid(row=2, column=3,pady=5,columnspan=2)

        self.botao_cadastro = tk.Button(frame_menu, text="CADASTRAR",bg="white",font=("cambria",12,"bold"), command=self.abrir_cadastro, width=15, height=2)
        self.botao_cadastro.grid(row=0, column=1, padx=5,pady=10,sticky="n")
        self.botao_delete = tk.Button(frame_menu, text="DELETAR",bg="white",font=("cambria",12,"bold"), command=self.abrir_delete, width=15, height=2)
        self.botao_delete.grid(row=1, column=1, padx= 5,pady= 10,sticky="n")
        
        self.palavrachave = tk.StringVar()

        pesquisa_label = tk.Label(frame_pesquisa, text="Pesquisar:", bg="white", font=("cambria", 12, "bold"))
        pesquisa_label.grid(row=1, column=1, pady=20, sticky="e")

        self.pesquisa_entry = tk.Entry(frame_pesquisa, textvariable=self.palavrachave,width=100, borderwidth=3)
        self.pesquisa_entry.grid(row=1, column=2, pady=20, sticky="w")

        self.palavrachave.trace_add("write",self.funcao_pesquisa)

        opcoes_PROCESSO = ["DESENHO", "PLANO DE CORTE", "CORTE", "ACABAMENTO", "CORTE", "PRÉ MONTAGEM", "COMFERENCIA", "ESTOQUE","MONTAGEM/OBRA"]
        combobox = ttk.Combobox(frame_pesquisa1, values=opcoes_PROCESSO)
        combobox.set("Selecione uma opção")
        combobox.grid(row=1, column=2,padx=15,pady=5,sticky="w")

        opcoes_status = ["PRODUÇÃO", "PRONTO", "ENTREGUE"]
        self.status_selecionado = ttk.Combobox(frame_pesquisa1, values=opcoes_status)
        self.status_selecionado.set(opcoes_status[0])
        self.status_selecionado.grid(row=2, column=2, padx=15,pady= 10,sticky="w")
        
        self.banco = banco_dado()
        resultados, colunas = self.banco.chamar_tabela()
        
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=20)
        for coluna in colunas:
            self.tabela.heading(coluna, text=coluna)
            self.tabela.column(coluna, width=130)
            self.tabela.grid(row=0, column=0, sticky="n")

        for row in resultados:
            self.tabela.insert('', 'end', values=row)

        image_logo1 = os.path.abspath("C:\\Users\\pedro\\Documents\\python\\K2KMOVELARIA\\logo.jpg")

        image_logo = Image.open(image_logo1)
        image_logo.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(image_logo)
        self.imagem_label_logo = tk.Label(frame_logo, image=photo,bg="white")
        self.imagem_label_logo.photo = photo
        self.imagem_label_logo.grid(row=1, column=2, columnspan=2, pady=10,sticky="n")
       ## self.imagem_label_logo.place(relx=0.5, rely=0.2, anchor="center")

        self.projetos.protocol("WM_DELETE_WINDOW",self.fechar_todas_janelas)
    
    def fechar_todas_janelas(self):
        self.master.destroy() 
    def funcao_pesquisa(self, *args):
        search_query = self.palavrachave.get()
    
    def abrir_cadastro(self):
        messagebox.showinfo("terminando","terminando")

    def abrir_delete(self):
        messagebox.showinfo("terminando","terminando")       
class almoxerifado:
    def __init__(self, master):
        self.master = master
        self.almoxerifado = tk.Toplevel(self.master)
        self.almoxerifado.title("K2K ALMOXERIFADO")
        largura_janela = 900
        altura_janela = 600
        largura_tela = master.winfo_screenwidth()
        altura_tela = master.winfo_screenheight()
        x = (largura_tela - largura_janela) // 2
        y = (altura_tela - altura_janela) // 2
        self.almoxerifado.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

        self.almoxerifado.grid_rowconfigure(2, weight=1)
        self.almoxerifado.grid_columnconfigure(3, weight=1)
        self.almoxerifado.configure(bg="white")

        frame_pesquisa = tk.Frame(self.almoxerifado,bg="white",relief="solid", borderwidth=1)
        frame_pesquisa.grid(row=0, column=2,sticky="n",pady=15,columnspan=2)
        
        frame_pesquisa1 = tk.Frame(frame_pesquisa,bg="white")
        frame_pesquisa1.grid(row=1, column=3,sticky="e",pady=5)

        frame_menu = tk.Frame(self.almoxerifado,bg="white")
        frame_menu.grid(row=2, column=3,sticky="n",pady=5,columnspan=2)

        frame_tabela = tk.Frame(self.almoxerifado,bg="white",relief="solid", borderwidth=1)
        frame_tabela.grid(row=2, column=2,sticky="n",pady=10,padx=10)

        frame_logo = tk.Frame(self.almoxerifado,bg="white")
        frame_logo.grid(row=2, column=3,pady=5,sticky="s",columnspan=2)

        self.botao_cadastro = tk.Button(frame_menu, text="CADASTRA",bg="white",font=("cambria",12,"bold"), command=self.abrir_cadastro, width=15, height=2)
        self.botao_cadastro.grid(row=0, column=1, padx=5,pady=10,sticky="n")
        self.botao_delete = tk.Button(frame_menu, text="DELETAR",bg="white",font=("cambria",12,"bold"), command=self.abrir_delete, width=15, height=2)
        self.botao_delete.grid(row=1, column=1, padx= 5,pady= 10,sticky="n")
        self.botao_pedidos = tk.Button(frame_menu, text="PEDIDOS",bg="white",font=("cambria",12,"bold"), command=self.abrir_delete, width=15, height=2)
        self.botao_pedidos.grid(row=2, column=1, padx= 5,pady= 10,sticky="n")
        self.botao_manutencao = tk.Button(frame_menu, text="MANUTENÇÃO",bg="white",font=("cambria",12,"bold"), command=self.abrir_delete, width=15, height=2)
        self.botao_manutencao.grid(row=3, column=1, padx= 5,pady= 10,sticky="n")


        self.palavrachave = tk.StringVar()

        pesquisa_label = tk.Label(frame_pesquisa, text="Pesquisar:", bg="white", font=("cambria", 12, "bold"))
        pesquisa_label.grid(row=1, column=1, pady=20, sticky="e")

        self.pesquisa_entry = tk.Entry(frame_pesquisa, textvariable=self.palavrachave,width=100, borderwidth=3)
        self.pesquisa_entry.grid(row=1, column=2, pady=20, sticky="w")

        self.palavrachave.trace_add("write",self.funcao_pesquisa)

        opcoes_PROCESSO = ["CHAPA", "FITA DE BORDO", "COLA", "EPI", "TINTAS", "FOLHAS / FORMICA", "PARAFUZO"]
        combobox = ttk.Combobox(frame_pesquisa1, values=opcoes_PROCESSO)
        combobox.set("Selecione uma opção")
        combobox.grid(row=1, column=2,padx=15,pady=5,sticky="w")

        opcoes_status = ["MATERIA PRIMA", "FERRAMENTAS"]
        self.status_selecionado = ttk.Combobox(frame_pesquisa1, values=opcoes_status)
        self.status_selecionado.set(opcoes_status[0])
        self.status_selecionado.grid(row=2, column=2, padx=15,pady= 10,sticky="w")

        colunas = ("Nome", "QUANTIDADE", "FABRICANTE","DATA VALIDADE")
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings",height=20)
        for coluna in colunas:
            self.tabela.heading(coluna, text=coluna)
            self.tabela.column(coluna, width=160)  # Defina a largura das colunas conforme necessário
        self.tabela.grid(row=0, column=0,sticky="n")

        image_logo = Image.open("C:\\Users\\pedro\\Documents\\python\\K2KMOVELARIA\\logo.jpg")
        image_logo.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(image_logo)
        self.imagem_almoxerifado_logo = tk.Label(frame_logo, image=photo,bg="white")
        self.imagem_almoxerifado_logo.photo = photo
        self.imagem_almoxerifado_logo.grid(row=1, column=2, columnspan=2, pady=10,sticky="n")
        
        self.almoxerifado.protocol("WM_DELETE_WINDOW",self.fechar_todas_janelas)
    
    def fechar_todas_janelas(self):
        self.master.destroy()

    def funcao_pesquisa(self, *args):
        search_query = self.palavrachave.get()
    
    def abrir_cadastro(self):
        messagebox.showinfo("terminando")
    def abrir_delete(self):
        messagebox.showinfo("terminando")
if __name__ == "__main__":
    root = tk.Tk()
    app = janela_login(root)
    root.mainloop()