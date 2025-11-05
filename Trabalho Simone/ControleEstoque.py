import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

ARQUIVO = "estoque.json"

def carregar_estoque():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salvar_estoque(estoque):
    with open(ARQUIVO, "w") as f:
        json.dump(estoque, f, indent=4)

def atualizar_lista():
    lista.delete(*lista.get_children())
    for i, produto in enumerate(carregar_estoque()):
        lista.insert("", "end", iid=i, values=(produto["nome"], produto["quantidade"], f'R$ {produto["preco"]:.2f}'))

def cadastrar_produto():
    nome = entrada_nome.get()
    quantidade = entrada_quantidade.get()
    preco = entrada_preco.get()

    if not nome or not quantidade or not preco:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return

    try:
        quantidade = int(quantidade)
        preco = float(preco)
    except ValueError:
        messagebox.showwarning("Erro", "Quantidade deve ser número inteiro e preço deve ser decimal.")
        return

    estoque = carregar_estoque()
    estoque.append({"nome": nome, "quantidade": quantidade, "preco": preco})
    salvar_estoque(estoque)
    atualizar_lista()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso.")

def remover_produto():
    item = lista.selection()
    if not item:
        messagebox.showwarning("Atenção", "Selecione um produto para remover.")
        return

    indice = int(item[0])
    estoque = carregar_estoque()
    del estoque[indice]
    salvar_estoque(estoque)
    atualizar_lista()
    messagebox.showinfo("Sucesso", "Produto removido com sucesso.")

def atualizar_produto():
    item = lista.selection()
    if not item:
        messagebox.showwarning("Atenção", "Selecione um produto para atualizar.")
        return

    indice = int(item[0])
    estoque = carregar_estoque()

    nome = entrada_nome.get()
    quantidade = entrada_quantidade.get()
    preco = entrada_preco.get()

    if not nome or not quantidade or not preco:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return

    try:
        estoque[indice]["nome"] = nome
        estoque[indice]["quantidade"] = int(quantidade)
        estoque[indice]["preco"] = float(preco)
    except ValueError:
        messagebox.showwarning("Erro", "Quantidade deve ser número inteiro e preço deve ser decimal.")
        return

    salvar_estoque(estoque)
    atualizar_lista()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")

def selecionar_item(event):
    item = lista.selection()
    if not item:
        return
    indice = int(item[0])
    estoque = carregar_estoque()
    produto = estoque[indice]

    entrada_nome.delete(0, tk.END)
    entrada_quantidade.delete(0, tk.END)
    entrada_preco.delete(0, tk.END)

    entrada_nome.insert(0, produto["nome"])
    entrada_quantidade.insert(0, produto["quantidade"])
    entrada_preco.insert(0, produto["preco"])

def limpar_campos():
    entrada_nome.delete(0, tk.END)
    entrada_quantidade.delete(0, tk.END)
    entrada_preco.delete(0, tk.END)

janela = tk.Tk()
janela.title("Controle de Estoque")
janela.geometry("520x400")
janela.resizable(False, False)

tk.Label(janela, text="Nome do Produto:").pack()
entrada_nome = tk.Entry(janela, width=40)
entrada_nome.pack()

tk.Label(janela, text="Quantidade:").pack()
entrada_quantidade = tk.Entry(janela, width=40)
entrada_quantidade.pack()

tk.Label(janela, text="Preço (R$):").pack()
entrada_preco = tk.Entry(janela, width=40)
entrada_preco.pack()

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

tk.Button(frame_botoes, text="Cadastrar", command=cadastrar_produto, width=12, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
tk.Button(frame_botoes, text="Atualizar", command=atualizar_produto, width=12, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5)
tk.Button(frame_botoes, text="Remover", command=remover_produto, width=12, bg="#f44336", fg="white").grid(row=0, column=2, padx=5)

colunas = ("Nome", "Quantidade", "Preço")
lista = ttk.Treeview(janela, columns=colunas, show="headings", height=10)
for col in colunas:
    lista.heading(col, text=col)
lista.pack(pady=10)

lista.bind("<<TreeviewSelect>>", selecionar_item)

atualizar_lista()

janela.mainloop()
