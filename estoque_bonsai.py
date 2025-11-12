import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# ======= CORES (tema Bonsai) =======
COR_FUNDO = "#F4EAD5"    # bege claro
COR_BOTAO = "#4A7856"    # verde musgo
COR_TEXTO = "#2E2E2E"    # cinza escuro
COR_BORDA = "#7A5230"    # marrom madeira

# ======= BANCO DE DADOS =======
def conectar():
    conexao = sqlite3.connect("estoque_bonsai.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()

def adicionar_produto(nome, quantidade, preco):
    conexao = sqlite3.connect("estoque_bonsai.db")
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
    conexao.commit()
    conexao.close()

def listar_produtos():
    conexao = sqlite3.connect("estoque_bonsai.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")
    dados = cursor.fetchall()
    conexao.close()
    return dados

def atualizar_produto(id, nome, quantidade, preco):
    conexao = sqlite3.connect("estoque_bonsai.db")
    cursor = conexao.cursor()
    cursor.execute("UPDATE produtos SET nome=?, quantidade=?, preco=? WHERE id=?", (nome, quantidade, preco, id))
    conexao.commit()
    conexao.close()

def remover_produto(id):
    conexao = sqlite3.connect("estoque_bonsai.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM produtos WHERE id=?", (id,))
    conexao.commit()
    conexao.close()

# ======= FUNÇÕES DA INTERFACE PRINCIPAL =======
def abrir_sistema():
    login_janela.destroy()

    janela = tk.Tk()
    janela.title("Estoque Bonsai - Alquimia do Bonsai")
    janela.geometry("550x450")
    janela.resizable(False, False)
    janela.config(bg=COR_FUNDO)

    def atualizar_lista():
        lista.delete(*lista.get_children())
        for produto in listar_produtos():
            lista.insert("", "end", iid=produto[0], values=(produto[1], produto[2], f"R$ {produto[3]:.2f}"))

    def cadastrar_produto():
        nome = entrada_nome.get()
        quantidade = entrada_quantidade.get()
        preco = entrada_preco.get()

        if not nome or not quantidade or not preco:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            quantidade = int(quantidade)
            preco = float(preco)
        except ValueError:
            messagebox.showwarning("Erro", "Quantidade deve ser número inteiro e preço deve ser decimal.")
            return

        adicionar_produto(nome, quantidade, preco)
        atualizar_lista()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

    def remover_item():
        item = lista.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um produto para remover.")
            return

        id_produto = int(item[0])
        remover_produto(id_produto)
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Produto removido com sucesso!")

    def atualizar_item():
        item = lista.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um produto para atualizar.")
            return

        id_produto = int(item[0])
        nome = entrada_nome.get()
        quantidade = entrada_quantidade.get()
        preco = entrada_preco.get()

        if not nome or not quantidade or not preco:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            quantidade = int(quantidade)
            preco = float(preco)
        except ValueError:
            messagebox.showwarning("Erro", "Quantidade deve ser número inteiro e preço deve ser decimal.")
            return

        atualizar_produto(id_produto, nome, quantidade, preco)
        atualizar_lista()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

    def selecionar_item(event):
        item = lista.selection()
        if not item:
            return
        id_produto = int(item[0])
        conexao = sqlite3.connect("estoque_bonsai.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, quantidade, preco FROM produtos WHERE id=?", (id_produto,))
        produto = cursor.fetchone()
        conexao.close()

        entrada_nome.delete(0, tk.END)
        entrada_quantidade.delete(0, tk.END)
        entrada_preco.delete(0, tk.END)

        entrada_nome.insert(0, produto[0])
        entrada_quantidade.insert(0, produto[1])
        entrada_preco.insert(0, produto[2])

    def limpar_campos():
        entrada_nome.delete(0, tk.END)
        entrada_quantidade.delete(0, tk.END)
        entrada_preco.delete(0, tk.END)

    # Labels e Entradas
    tk.Label(janela, text="Nome do Produto:", bg=COR_FUNDO, fg=COR_TEXTO).pack()
    entrada_nome = tk.Entry(janela, width=45)
    entrada_nome.pack()

    tk.Label(janela, text="Quantidade:", bg=COR_FUNDO, fg=COR_TEXTO).pack()
    entrada_quantidade = tk.Entry(janela, width=45)
    entrada_quantidade.pack()

    tk.Label(janela, text="Preço (R$):", bg=COR_FUNDO, fg=COR_TEXTO).pack()
    entrada_preco = tk.Entry(janela, width=45)
    entrada_preco.pack()

    # Botões
    frame_botoes = tk.Frame(janela, bg=COR_FUNDO)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Cadastrar", command=cadastrar_produto, width=12, bg=COR_BOTAO, fg="white", relief="flat").grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="Atualizar", command=atualizar_item, width=12, bg="#2196F3", fg="white", relief="flat").grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="Remover", command=remover_item, width=12, bg="#f44336", fg="white", relief="flat").grid(row=0, column=2, padx=5)

    # Lista de produtos
    colunas = ("Nome", "Quantidade", "Preço")
    lista = ttk.Treeview(janela, columns=colunas, show="headings", height=10)
    for col in colunas:
        lista.heading(col, text=col)
    lista.pack(pady=10)

    lista.bind("<<TreeviewSelect>>", selecionar_item)

    # Inicializa banco e carrega lista
    conectar()
    atualizar_lista()

    janela.mainloop()

# ======= TELA DE LOGIN =======
def fazer_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()

    if usuario == "admin" and senha == "1234":
        abrir_sistema()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

login_janela = tk.Tk()
login_janela.title("Login - Estoque Bonsai")
login_janela.geometry("300x250")
login_janela.resizable(False, False)
login_janela.config(bg=COR_FUNDO)

tk.Label(login_janela, text="LOGIN", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 14, "bold")).pack(pady=10)
tk.Label(login_janela, text="Usuário:", bg=COR_FUNDO, fg=COR_TEXTO).pack()
entrada_usuario = tk.Entry(login_janela, width=30)
entrada_usuario.pack(pady=5)

tk.Label(login_janela, text="Senha:", bg=COR_FUNDO, fg=COR_TEXTO).pack()
entrada_senha = tk.Entry(login_janela, width=30, show="*")
entrada_senha.pack(pady=5)

tk.Button(login_janela, text="Entrar", command=fazer_login, bg=COR_BOTAO, fg="white", width=15).pack(pady=15)

login_janela.mainloop()
