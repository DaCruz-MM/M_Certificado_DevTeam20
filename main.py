import Cadastro_de_Ferramentas as DB_F
import Cadastro_de_Funcionarios as DB_T
import Cadastro_de_Reservas as DB_R
from datetime import datetime
from tkinter import *
from tkinter import ttk


class interface_geral():
    def __init__(self):
        self.janela_principal = Tk()
        self.janela_principal.title("Interface Missão")
        self.janela_principal.resizable(False, False)
        # self.janela_principal.geometry("300x400")
        self.tabcontrol = ttk.Notebook(self.janela_principal)
        self.tabcontrol.pack(expand=1, fill="both")
        ferramenta(self.tabcontrol, self.janela_principal)
        funcionarios(self.tabcontrol, self.janela_principal)
        reservas(self.tabcontrol, self.janela_principal)
        self.janela_principal.mainloop()


#           FERRAMENTAS


class ferramenta():
    def __init__(self, tabcontrol, janela):
        self.janela = janela
        self.frame_ferramentas = Frame(tabcontrol)
        self.frame_ferramentas.pack(fill='both', expand=True)
        tabcontrol.add(self.frame_ferramentas, text='Ferramentas')
        Frame(self.frame_ferramentas, height=2, bd=1).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        Label(self.frame_ferramentas, text='Coluna:').grid(row=1, column=0, sticky="w")
        self.coluna_d = StringVar()
        ttk.Combobox(self.frame_ferramentas, textvariable=self.coluna_d, values=DB_F.pegar_colunas()).grid(row=2,
                                                                                                           column=0)
        Label(self.frame_ferramentas, text='Filtro:').grid(row=1, column=1, sticky="w")
        self.filtro_d = StringVar()
        Entry(self.frame_ferramentas, textvariable=self.filtro_d, bg='#BDBDBD').grid(row=2, column=1, sticky="w")
        Frame(self.frame_ferramentas, height=2, bd=1).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        Button(self.frame_ferramentas, width=10, text='Exibir', command=self.exibir).grid(row=4, column=0, columnspan=1)
        Button(self.frame_ferramentas, width=10, text='Adicionar', command=self.adicionar).grid(row=4, column=1,
                                                                                                columnspan=1)
        self.textd_f = []
        Frame(self.frame_ferramentas, height=2, bd=1).grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.frame_info_ferramenta = Frame(self.frame_ferramentas, relief=GROOVE, borderwidth=2, bg='#BDBDBD')
        self.frame_info_ferramenta.grid(row=6, column=0, columnspan=2, rowspan=4, sticky="we")
        self.index = 0
        for i in range(len(DB_F.pegar_colunas())):
            colunas = DB_F.pegar_colunas()
            Label(self.frame_info_ferramenta, text=f"{colunas[i]}:", bg='#BDBDBD').grid(row=(i), column=0, sticky="wn")
            self.textd_f.insert(i, StringVar())
            self.text = Label(self.frame_info_ferramenta, wraplength=100, justify=LEFT, textvariable=self.textd_f[i], bg='#BDBDBD').grid(row=(i), column=1,
                                                                                               sticky="w")
            self.textd_f[i].set("null")
            self.index = i + 1
        Label(self.frame_info_ferramenta, wraplength=200, justify=LEFT, text="Reservas:", bg='#BDBDBD').grid(row=self.index, column=0, sticky="w")
        self.textd_f.insert(self.index, StringVar())
        Label(self.frame_info_ferramenta, textvariable=self.textd_f[self.index], bg='#BDBDBD').grid(row=self.index, column=1,
                                                                                               sticky="wn")
        self.textd_f[self.index].set("null")
        self.tree = ttk.Treeview(self.frame_ferramentas, columns=['1', '2', '3'], show='headings')
        self.tree.grid(row=0, column=4, rowspan=9, columnspan=2, sticky='nsew')
        self.tree.column('1', width=20)
        self.tree.column('2', width=80)
        self.tree.column('3', width=60)
        self.tree.heading('1', text='Id')
        self.tree.heading('2', text='Ferramenta')
        self.tree.heading('3', text='Reservas')
        self.sb = Scrollbar(self.tree, orient=VERTICAL)
        self.sb.pack(side=RIGHT, fill=Y)
        self.atualizar_arvore()
        self.frame_button_ferramenta = Frame(self.frame_ferramentas, relief=GROOVE, borderwidth=2, bg='#BDBDBD')
        self.frame_button_ferramenta.grid(row=9, column=4, columnspan=1, rowspan=2, sticky="we")
        Button(self.frame_button_ferramenta, width=10, text='Selecionar', command=self.selecionar).grid(row=8, column=4)
        Button(self.frame_button_ferramenta, width=10, text='Remover', command=self.remover).grid(row=8, column=5)
        Button(self.frame_button_ferramenta, width=10, text='Editar', command=self.editar).grid(row=9, column=4)
        Button(self.frame_button_ferramenta, width=10, text='Limpar', command=self.limpar).grid(row=9, column=5)

    def atualizar_arvore(self):
        self.tree.delete(*self.tree.get_children())
        lista_ferramentas = DB_F.pegar_ferramentas()
        for i in range(len(lista_ferramentas)):
            self.tree.insert(parent='', index=i, iid=i,
                             values=(lista_ferramentas[i][0], lista_ferramentas[i][1],
                                len(DB_R.selecionar_reservas(DB_R.pegar_colunas()[1], lista_ferramentas[i][0]))))

    def exibir(self):
        self.coluna = self.coluna_d.get()
        self.filtro = self.filtro_d.get()
        if self.coluna and self.filtro:
            item = DB_F.selecionar_ferramenta(self.coluna, self.filtro)
            try:
                item = item[0]
                for i in range(len(item)):
                    self.textd_f[i].set(item[i])
                self.textd_f[self.index].set(f"{len(DB_R.selecionar_reservas(DB_R.pegar_colunas()[1], item[0]))}")
            except:
                print("Erro:", sys.exc_info()[0])

    def adicionar(self):
        top = Toplevel(self.janela)
        adicionar_ferramenta(top, self)
        self.atualizar_arvore()

    def selecionar(self):
        self.item = self.tree.item(self.tree.focus(), 'values')
        if self.item:
            item = DB_F.selecionar_ferramenta(DB_F.pegar_colunas()[0], self.item[0])
            try:
                item = item[0]
                for i in range(len(item)):
                    self.textd_f[i].set(item[i])
                self.textd_f[self.index].set(f"{len(DB_R.selecionar_reservas(DB_R.pegar_colunas()[1], item[0]))}")
            except:
                print("Erro:", sys.exc_info()[0])

    def remover(self):
        self.item = self.tree.item(self.tree.focus(), 'values')
        if self.item:
            DB_F.remover_ferramenta(DB_F.pegar_colunas()[0], self.item[0])
        self.atualizar_arvore()

    def editar(self):
        self.item = self.tree.item(self.tree.focus(), 'values')
        if self.item:
            item = (DB_F.selecionar_ferramenta(DB_F.pegar_colunas()[0], self.item[0]))[0]
            top = Toplevel(self.janela)
            editar_ferramenta(top, item, self)
            self.atualizar_arvore()

    def limpar(self):
        top = Toplevel(self.janela)
        janela_confirm(top, "Essa opção irá remover todas as ferramentas.\n"
                                               "Tem certeza que quer fazer isso?", 1, self)

    def limpar_1(self):
        top = Toplevel(self.janela)
        janela_confirm(top, "Tem certeza mesmo?", 2, self)

    def limpar_2(self):
        top = Toplevel(self.janela)
        janela_confirm(top, "Absoluta?", 3, self)

    def limpar_3(self):
        DB_F.limpar_ferramentas()

    def grab(self):
        self.janela.grab_set()


class adicionar_ferramenta():
    def __init__(self, janela, app):
        self.app = app
        self.janela_adicionar_ferramenta = janela
        self.janela_adicionar_ferramenta.grab_set()
        self.janela_adicionar_ferramenta.title("Registrar Ferramenta")
        self.janela_adicionar_ferramenta.resizable(False, False)
        Label(self.janela_adicionar_ferramenta, text="Preencha os campos").grid(row=0, column=0, columnspan=2)
        self.rows = ['Descrição da Ferramenta:', 'Fabricante:', 'Voltagem de uso:', 'Part Number:', 'Tamanho:', 'Unidade de medida:', 'Tipo de ferramenta:', 'Material da ferramenta:', 'Tempo máximo de reserva:']
        self.info_f = []
        for i in range(len(self.rows)):
            Label(self.janela_adicionar_ferramenta, text=self.rows[i]).grid(row=i+1, column=0, sticky="w")
            self.info_f.insert(i, StringVar())
            Entry(self.janela_adicionar_ferramenta, textvariable=self.info_f[i]).grid(row=i+1, column=1, sticky="w")
        Button(self.janela_adicionar_ferramenta, width=10, text='Registrar', command=self.registrar).grid(row=10, column=0)
        Button(self.janela_adicionar_ferramenta, width=10, text='Cancelar', command=self.cancelar).grid(row=10, column=1)

    def registrar(self):
        lista_f = []
        for i in range(len(self.info_f)):
            item = self.info_f[i].get()
            lista_f.insert(i, item)

        if int(len(lista_f[0])) > 60:
            top = Toplevel(self.janela_adicionar_ferramenta)
            janela_erro(top, f'O limite de caracteres do campo \'{self.rows[0]}\' é 60', self)
        elif int(len(lista_f[1])) > 30:
            top = Toplevel(self.janela_adicionar_ferramenta)
            janela_erro(top, f'O limite de caracteres do campo \'{self.rows[1]}\' é 30', self)
        elif int(len(lista_f[2])) > 15:
            top = Toplevel(self.janela_adicionar_ferramenta)
            janela_erro(top, f'O limite de caracteres do campo \'{self.rows[2]}\' é 15', self)
        elif int(len(lista_f[3])) > 25:
            top = Toplevel(self.janela_adicionar_ferramenta)
            janela_erro(top, f'O limite de caracteres do campo \'{self.rows[3]}\' é 25', self)
        elif int(len(lista_f[4])) > 20:
            top = Toplevel(self.janela_adicionar_ferramenta)
            janela_erro(top, f'O limite de caracteres do campo \'{self.rows[4]}\' é 20', self)
        elif int(len(lista_f[5])) > 15:
            top = Toplevel(self.janela_adicionar_ferramenta)
            janela_erro(top, f'O limite de caracteres do campo \'{self.rows[5]}\' é 15', self)
        elif int(len(lista_f[6])) > 15:
            top = Toplevel(self.janela_adicionar_ferramenta)
            janela_erro(top, f'O limite de caracteres do campo \'{self.rows[6]}\' é 15', self)
        elif int(len(lista_f[7])) > 15:
            top = Toplevel(self.janela_adicionar_ferramenta)
            janela_erro(top, f'O limite de caracteres do campo \'{self.rows[7]}\' é 15', self)
        elif not (lista_f[8]).isnumeric():
            top = Toplevel(self.janela_adicionar_ferramenta)
            janela_erro(top, f'Informação invalida\nNo campo \'{self.rows[8]}\' só é aceito numeros.', self)
        else:
            DB_F.adicionar_ferramenta(lista_f)
            self.app.atualizar_arvore()
            self.janela_adicionar_ferramenta.destroy()

    def cancelar(self):
        self.janela_adicionar_ferramenta.destroy()

    def grab(self):
        self.janela_adicionar_ferramenta.grab_set()


class editar_ferramenta():
    def __init__(self, janela, item, app):
        self.app = app
        self.item = item
        self.janela_editar_ferramenta = janela
        self.janela_editar_ferramenta.grab_set()
        self.janela_editar_ferramenta.title("Editar Ferramenta")
        self.janela_editar_ferramenta.resizable(False, False)
        Label(self.janela_editar_ferramenta, text="Preencha os campos").grid(row=0, column=0, columnspan=2)
        rows = ['Descrição da Ferramenta:', 'Fabricante:', 'Voltagem de uso:', 'Part Number:', 'Tamanho:', 'Unidade de medida:', 'Tipo de ferramenta:', 'Material da ferramenta:', 'Tempo máximo de reserva:']
        self.info_f = []
        for i in range(len(rows)):
            Label(self.janela_editar_ferramenta, text=rows[i]).grid(row=i+1, column=0, sticky="w")
            self.info_f.insert(i, StringVar())
            self.info_f[i].set(self.item[i+1])
            Entry(self.janela_editar_ferramenta, textvariable=self.info_f[i]).grid(row=i+1, column=1, sticky="w")
        Button(self.janela_editar_ferramenta, width=10, text='Editar', command=self.editar).grid(row=10, column=0)
        Button(self.janela_editar_ferramenta, width=10, text='Cancelar', command=self.cancelar).grid(row=10, column=1)

    def editar(self):
        for i in range(len(self.info_f)):
            item = self.info_f[i].get()
            DB_F.editar_ferramenta(DB_F.pegar_colunas()[0], self.item[0], DB_F.pegar_colunas()[i+1], item)
        self.app.atualizar_arvore()
        self.janela_editar_ferramenta.destroy()

    def cancelar(self):
        self.janela_editar_ferramenta.destroy()

    def grab(self):
        self.janela_editar_ferramenta.grab_set()


#           FUNCIONARIOS


class funcionarios():
    def __init__(self, tabcontrol, janela):
        self.janela = janela
        self.frame = Frame(tabcontrol)
        self.frame.pack(fill='both', expand=True)
        tabcontrol.add(self.frame, text='Funcionarios')
        Frame(self.frame, height=2, bd=1).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        Label(self.frame, text='Coluna:').grid(row=1, column=0, sticky="w")
        self.coluna_d = StringVar()
        ttk.Combobox(self.frame, textvariable=self.coluna_d, values=DB_T.pegar_colunas()).grid(row=2,
                                                                                                           column=0)
        Label(self.frame, text='Filtro:').grid(row=1, column=1, sticky="w")
        self.filtro_d = StringVar()
        Entry(self.frame, textvariable=self.filtro_d, bg='#BDBDBD').grid(row=2, column=1, sticky="w")
        Frame(self.frame, height=2, bd=1).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        Button(self.frame, width=10, text='Exibir', command=self.exibir).grid(row=4, column=0, columnspan=1)
        Button(self.frame, width=10, text='Adicionar', command=self.adicionar).grid(row=4, column=1,
                                                                                                columnspan=1)
        self.textd_f = []
        Frame(self.frame, height=2, bd=1).grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.frame_info = Frame(self.frame, relief=GROOVE, borderwidth=2, bg='#BDBDBD')
        self.frame_info.grid(row=6, column=0, columnspan=2, rowspan=4, sticky="we")
        for i in range(len(DB_T.pegar_colunas())):
            colunas = DB_T.pegar_colunas()
            Label(self.frame_info, text=f"{colunas[i]}:", bg='#BDBDBD').grid(row=(i), column=0, sticky="wn")
            self.textd_f.insert(i, StringVar())
            Label(self.frame_info, wraplength=100, justify=LEFT, textvariable=self.textd_f[i], bg='#BDBDBD').grid(row=(i), column=1,
                                                                                               sticky="wn")
            self.textd_f[i].set("null")
        self.tree = ttk.Treeview(self.frame, columns=['1', '2', '3'], show='headings')
        self.tree.grid(row=0, column=4, rowspan=9, columnspan=2, sticky='nsew')
        self.tree.column('1', width=20)
        self.tree.column('2', width=80)
        self.tree.column('3', width=60)
        self.tree.heading('1', text='Id')
        self.tree.heading('2', text='Funcionario')
        self.tree.heading('3', text='Grupo')
        self.sb = Scrollbar(self.tree, orient=VERTICAL)
        self.sb.pack(side=RIGHT, fill=Y)
        self.atualizar_arvore()
        self.frame_button = Frame(self.frame, relief=GROOVE, borderwidth=2, bg='#BDBDBD')
        self.frame_button.grid(row=9, column=4, columnspan=1, rowspan=2, sticky="we")
        Button(self.frame_button, width=10, text='Selecionar', command=self.selecionar).grid(row=8, column=4)
        Button(self.frame_button, width=10, text='Remover', command=self.remover).grid(row=8, column=5)
        Button(self.frame_button, width=10, text='Editar', command=self.editar).grid(row=9, column=4)
        Button(self.frame_button, width=10, text='Limpar', command=self.limpar).grid(row=9, column=5)

    def atualizar_arvore(self):
        self.tree.delete(*self.tree.get_children())
        lista = DB_T.pegar_funcionarios()
        for i in range(len(lista)):
            self.tree.insert(parent='', index=i, iid=i,
                             values=(lista[i][0], lista[i][1], lista[i][5]))

    def exibir(self):
        self.coluna = self.coluna_d.get()
        self.filtro = self.filtro_d.get()
        if self.coluna and self.filtro:
            item = DB_T.selecionar_funcionarios(self.coluna, self.filtro)
            try:
                item = item[0]
                for i in range(len(item)):
                    self.textd_f[i].set(item[i])
            except:
                print("Erro:", sys.exc_info()[0])

    def adicionar(self):
        top = Toplevel(self.janela)
        adicionar_funcionario(top, self)
        self.atualizar_arvore()

    def selecionar(self):
        self.item = self.tree.item(self.tree.focus(), 'values')
        if self.item:
            item = DB_T.selecionar_funcionarios(DB_T.pegar_colunas()[0], self.item[0])
            try:
                item = item[0]
                for i in range(len(item)):
                    self.textd_f[i].set(item[i])
            except:
                print("Erro:", sys.exc_info()[0])

    def remover(self):
        self.item = self.tree.item(self.tree.focus(), 'values')
        if self.item:
            DB_T.remover_funcionarios(DB_T.pegar_colunas()[0], self.item[0])
        self.atualizar_arvore()

    def editar(self):
        self.item = self.tree.item(self.tree.focus(), 'values')
        if self.item:
            item = (DB_T.selecionar_funcionarios(DB_T.pegar_colunas()[0], self.item[0]))[0]
            top = Toplevel(self.janela)
            editar_funcionario(top, item, self)
            self.atualizar_arvore()

    def limpar(self):
        top = Toplevel(self.janela)
        janela_confirm(top, "Essa opção irá remover todas os funcionarios.\n"
                            "Tem certeza que quer fazer isso?", 1, self)

    def limpar_1(self):
        top = Toplevel(self.janela)
        janela_confirm(top, "Tem certeza mesmo?", 2, self)

    def limpar_2(self):
        top = Toplevel(self.janela)
        janela_confirm(top, "Absoluta?", 3, self)

    def limpar_3(self):
        DB_T.limpar_funcionarios()

    def grab(self):
        self.janela.grab_set()


class adicionar_funcionario():
    def __init__(self, janela, app):
        self.app = app
        self.janela_adicionar = janela
        self.janela_adicionar.grab_set()
        self.janela_adicionar.title("Registrar Funcionario")
        self.janela_adicionar.resizable(False, False)
        Label(self.janela_adicionar, text="Preencha os campos").grid(row=0, column=0, columnspan=2)
        self.rows = ['Nome do Funcionario:', 'CPF do funcionário:', 'Telefone:', 'Turno:', 'Grupo:']
        self.info = []
        for i in range(len(self.rows)):
            Label(self.janela_adicionar, text=self.rows[i]).grid(row=i+1, column=0, sticky="w")
            self.info.insert(i, StringVar())
            Entry(self.janela_adicionar, textvariable=self.info[i]).grid(row=i+1, column=1, sticky="w")
        Button(self.janela_adicionar, width=10, text='Registrar', command=self.registrar).grid(row=10, column=0)
        Button(self.janela_adicionar, width=10, text='Cancelar', command=self.cancelar).grid(row=10, column=1)

    def registrar(self):
        lista_f = []
        for i in range(len(self.info)):
            item = self.info[i].get()
            lista_f.insert(i, item)
        if int(len(lista_f[0])) > 40:
            top = Toplevel(self.janela_adicionar)
            janela_erro(top, f'O limite de caracteres do campo \'{self.rows[1]}\' é 40', self)
        elif not self.cpf_validate(lista_f[1]):
            top = Toplevel(self.janela_adicionar)
            janela_erro(top, f'Esse CPF é invalido', self)
        elif int(len(lista_f[4])) > 30:
            top = Toplevel(self.janela_adicionar)
            janela_erro(top, f'O limite de caracteres do campo \'{self.rows[4]}\' é 30', self)
        else:
            DB_T.adicionar_funcionarios(lista_f)
            self.app.atualizar_arvore()
            self.janela_adicionar.destroy()

    def cpf_validate(self, numbers):
        numbers = str(numbers)
        cpf = [int(char) for char in numbers if char.isdigit()]
        if len(cpf) != 11:
            return False
        if cpf == cpf[::-1]:
            return False
        for i in range(9, 11):
            value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != cpf[i]:
                return False
        return True

    def cancelar(self):
        self.janela_adicionar.destroy()

    def grab(self):
        self.janela_adicionar.grab_set()


class editar_funcionario():
    def __init__(self, janela, item, app):
        self.app = app
        self.item = item
        self.janela_editar = janela
        self.janela_editar.grab_set()
        self.janela_editar.title("Editar Funcionario")
        self.janela_editar.resizable(False, False)
        Label(self.janela_editar, text="Preencha os campos").grid(row=0, column=0, columnspan=2)
        rows = ['Nome do Funcionario:', 'CPF do funcionário:', 'Telefone:', 'Turno:', 'Grupo:']
        self.info = []
        for i in range(len(rows)):
            Label(self.janela_editar, text=rows[i]).grid(row=i+1, column=0, sticky="w")
            self.info.insert(i, StringVar())
            self.info[i].set(self.item[i+1])
            Entry(self.janela_editar, textvariable=self.info[i]).grid(row=i+1, column=1, sticky="w")
        Button(self.janela_editar, width=10, text='Editar', command=self.editar).grid(row=10, column=0)
        Button(self.janela_editar, width=10, text='Cancelar', command=self.cancelar).grid(row=10, column=1)

    def editar(self):
        for i in range(len(self.info)):
            item = self.info[i].get()
            DB_T.editar_funcionarios(DB_T.pegar_colunas()[0], self.item[0], DB_T.pegar_colunas()[i+1], item)
        self.app.atualizar_arvore()
        self.janela_editar.destroy()

    def cancelar(self):
        self.janela_editar.destroy()

    def grab(self):
        self.janela_editar.grab_set()

#           RESERVAS


class reservas():
    def __init__(self, tabcontrol, janela):
        self.janela = janela
        self.frame = Frame(tabcontrol)
        self.frame.pack(fill='both', expand=True)
        tabcontrol.add(self.frame, text='Reservas')
        Frame(self.frame, height=2, bd=1).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        Label(self.frame, text='Coluna:').grid(row=1, column=0, sticky="w")
        self.coluna_d = StringVar()
        ttk.Combobox(self.frame, textvariable=self.coluna_d, values=DB_T.pegar_colunas()).grid(row=2,
                                                                                                           column=0)
        Label(self.frame, text='Filtro:').grid(row=1, column=1, sticky="w")
        self.filtro_d = StringVar()
        Entry(self.frame, textvariable=self.filtro_d, bg='#BDBDBD').grid(row=2, column=1, sticky="w")
        Frame(self.frame, height=2, bd=1).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        Button(self.frame, width=10, text='Exibir', command=self.exibir).grid(row=4, column=0, columnspan=1)
        Button(self.frame, width=10, text='Adicionar', command=self.adicionar).grid(row=4, column=1,
                                                                                                columnspan=1)
        self.textd_f = []
        Frame(self.frame, height=2, bd=1).grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.frame_info = Frame(self.frame, relief=GROOVE, borderwidth=2, bg='#BDBDBD')
        self.frame_info.grid(row=6, column=0, columnspan=2, rowspan=4, sticky="we")
        for i in range(len(DB_R.pegar_colunas())):
            colunas = DB_R.pegar_colunas()
            Label(self.frame_info, wraplength=100, justify=LEFT, text=f"{colunas[i]}:", bg='#BDBDBD').grid(row=(i), column=0, sticky="wn")
            self.textd_f.insert(i, StringVar())
            Label(self.frame_info, wraplength=100, justify=LEFT, textvariable=self.textd_f[i], bg='#BDBDBD').grid(row=(i), column=1,
                                                                                               sticky="wn")
            self.textd_f[i].set("null")
        self.tree = ttk.Treeview(self.frame, columns=['1', '2', '3'], show='headings')
        self.tree.grid(row=0, column=4, rowspan=9, columnspan=2, sticky='nsew')
        self.tree.column('1', width=20)
        self.tree.column('2', width=80)
        self.tree.column('3', width=60)
        self.tree.heading('1', text='Id')
        self.tree.heading('2', text='Nome')
        self.tree.heading('3', text='Ferramenta')
        self.sb = Scrollbar(self.tree, orient=VERTICAL)
        self.sb.pack(side=RIGHT, fill=Y)
        self.atualizar_arvore()
        self.frame_button = Frame(self.frame, relief=GROOVE, borderwidth=2, bg='#BDBDBD')
        self.frame_button.grid(row=9, column=4, columnspan=1, rowspan=2, sticky="we")
        self.button_1 = Button(self.frame_button, width=10, text='Selecionar', command=self.selecionar).grid(row=8, column=4)
        self.button_2 = Button(self.frame_button, width=10, text='Remover', command=self.remover).grid(row=8, column=5)
        self.button_3 = Button(self.frame_button, width=10, state= DISABLED, text='Editar', command=self.editar).grid(row=9, column=4)
        self.button_4 = Button(self.frame_button, width=10, text='Limpar', command=self.limpar).grid(row=9, column=5)

    def atualizar_arvore(self):
        self.tree.delete(*self.tree.get_children())
        lista = DB_R.pegar_reservas()
        for i in range(len(lista)):
            self.tree.insert(parent='', index=i, iid=i,
                             values=(lista[i][0], lista[i][5], lista[i][1]))

    def exibir(self):
        self.coluna = self.coluna_d.get()
        self.filtro = self.filtro_d.get()
        if self.coluna and self.filtro:
            item = DB_R.selecionar_reservas(self.coluna, self.filtro)
            try:
                item = item[0]
                for i in range(len(item)):
                    self.textd_f[i].set(item[i])
            except:
                print("Erro:", sys.exc_info()[0])

    def adicionar(self):
        top = Toplevel(self.janela)
        adicionar_reserva(top, self)
        self.atualizar_arvore()

    def selecionar(self):
        self.item = self.tree.item(self.tree.focus(), 'values')
        if self.item:
            item = DB_R.selecionar_reservas(DB_R.pegar_colunas()[0], self.item[0])
            try:
                item = item[0]
                for i in range(len(item)):
                    self.textd_f[i].set(item[i])
            except:
                print("Erro:", sys.exc_info()[0])

    def remover(self):
        self.item = self.tree.item(self.tree.focus(), 'values')
        if self.item:
            DB_R.remover_reservas(DB_R.pegar_colunas()[0], self.item[0])
        self.atualizar_arvore()

    def editar(self):
        self.item = self.tree.item(self.tree.focus(), 'values')
        if self.item:
            item = (DB_R.selecionar_reservas(DB_R.pegar_colunas()[0], self.item[0]))[0]
            top = Toplevel(self.janela)
            editar_reserva(top, item, self)
            self.atualizar_arvore()

    def limpar(self):
        top = Toplevel(self.janela)
        janela_confirm(top, "Essa opção irá remover todas as reservas.\n"
                                               "Tem certeza que quer fazer isso?", 1, self)

    def limpar_1(self):
        top = Toplevel(self.janela)
        janela_confirm(top, "Tem certeza mesmo?", 2, self)

    def limpar_2(self):
        top = Toplevel(self.janela)
        janela_confirm(top, "Absoluta?", 3, self)

    def limpar_3(self):
        DB_R.limpar_reservas()

    def grab(self):
        self.janela.grab_set()


class adicionar_reserva():
    def __init__(self, janela, app):
        self.app = app
        self.janela_adicionar = janela
        self.janela_adicionar.grab_set()
        self.janela_adicionar.title("Fazer Reserva")
        self.janela_adicionar.resizable(False, False)
        Label(self.janela_adicionar, text="Preencha os campos").grid(row=0, column=0, columnspan=2)
        rows = ['Código da ferramenta:', 'Descrição da solicitação:', 'Data e hora de retirada:', 'Data e hora para devolução:', 'Id do responsável pela retirada:']
        self.info = []
        for i in range(len(rows)):
            Label(self.janela_adicionar, text=rows[i]).grid(row=i+1, column=0, sticky="w")
            self.info.insert(i, StringVar())
            Entry(self.janela_adicionar, textvariable=self.info[i]).grid(row=i+1, column=1, sticky="w")
        Button(self.janela_adicionar, width=10, text='Registrar', command=self.registrar).grid(row=10, column=0)
        Button(self.janela_adicionar, width=10, text='Cancelar', command=self.cancelar).grid(row=10, column=1)

    def registrar(self):
        lista_f = []
        erro = False
        for i in range(len(self.info)):
            if i == 0:
                try:
                    item = self.info[i].get()
                    item = (DB_F.selecionar_ferramenta(DB_F.pegar_colunas()[0], item))[0][0]
                    lista_f.insert(i, item)
                except(IndexError):
                    erro = "Id invalido!\nEssa ferramenta não existe."
                    break
            elif i == 2 and i == 3:
                try:
                    item = self.info[i].get()
                    data_hora = datetime.strptime(item, '%d/%m/%Y %H:%M')
                    lista_f.insert(i, data_hora)
                except(ValueError):
                    erro = "Essa data é invalida.\nExemplo: 05/09/2022 06:00"
                    break
            elif i == 4:
                try:
                    item = self.info[i].get()
                    item = (DB_T.selecionar_funcionarios(DB_T.pegar_colunas()[0], item))[0][1]
                    lista_f.insert(i, item)
                except(IndexError):
                    erro = "Id invalido!\nEsse funcionario não existe."
                    break
            else:
                item = self.info[i].get()
                lista_f.insert(i, item)
        reservas = DB_R.selecionar_reservas(DB_R.pegar_colunas()[1], lista_f[0])
        for i in reservas:
            t1, t2, t3, t4 = lista_f[2], lista_f[3], i[3], i[4]
            check = self.disponibilidade(t1, t2, t3, t4)
            if not check and not erro:
                erro = f"Ferramenta indisponivel!\nEssa ferramenta já esta reservada nessa data hora.\n\
                Ferramenta indisponivel a partir de {t3} até {t4}"
        check = self.atualidade(lista_f[2], lista_f[3])
        if not check and not erro:
            erro = f"Essa data e hora é invalida!\nNão se pode reservar uma ferramenta em um dia e hora que passou"
        hora = (DB_F.selecionar_ferramenta(DB_F.pegar_colunas()[0], lista_f[0]))
        for i in hora:
            check = self.limite_de_reserva(lista_f[2], lista_f[3], int(i[9]))
            if not check and not erro:
                erro = f"Essa ferramenta não pode ter uma reserva com mais de {i[9]} horas"
        if not erro:
            DB_R.adicionar_reservas(lista_f)
            self.app.atualizar_arvore()
            self.janela_adicionar.destroy()
        else:
            top = Toplevel(self.janela_adicionar)
            self.janela_erro = janela_erro(top, erro, self)

    def disponibilidade(self, t1, t2, t3, t4):
        t1 = datetime.strptime(t1, '%d/%m/%Y %H:%M')
        t2 = datetime.strptime(t2, '%d/%m/%Y %H:%M')
        t3 = datetime.strptime(t3, '%d/%m/%Y %H:%M')
        t4 = datetime.strptime(t4, '%d/%m/%Y %H:%M')
        if ((t1 - t3).total_seconds()) < 0 and ((t2 - t3).total_seconds()) < 0:
            return True
        elif ((t1 - t4).total_seconds()) > 0 and ((t2 - t4).total_seconds()) > 0:
            return True
        else:
            return False

    def atualidade(self, t1, t2):
        t1 = datetime.strptime(t1, '%d/%m/%Y %H:%M')
        t2 = datetime.strptime(t2, '%d/%m/%Y %H:%M')
        t3 = datetime.now()
        if ((t1 - t3).total_seconds()) > 0 and ((t2 - t3).total_seconds()) > 0:
            return True
        else:
            return False

    def limite_de_reserva(self, t1, t2, t3):
        t1 = datetime.strptime(t1, '%d/%m/%Y %H:%M')
        t2 = datetime.strptime(t2, '%d/%m/%Y %H:%M')
        t3 = 60*(60*(t3))
        t4 = ((t2 - t1).total_seconds())
        if t4 < (t3+1):
            return True
        else:
            return False

    def cancelar(self):
        self.janela_adicionar.destroy()

    def grab(self):
        self.janela_adicionar.grab_set()


class editar_reserva():
    def __init__(self, janela, item, app):
        self.app = app
        self.item = item
        self.janela_editar = janela
        self.janela_editar.grab_set()
        self.janela_editar.title("Editar Reserva")
        self.janela_editar.resizable(False, False)
        Label(self.janela_editar, text="Preencha os campos").grid(row=0, column=0, columnspan=2)
        rows = ['Código da ferramenta:', 'Descrição da solicitação:', 'Data e hora da retirada:', 'Data e hora prevista de devolução:', 'Técnico responsável pela retirada:']
        self.info = []
        for i in range(len(rows)):
            Label(self.janela_editar, text=rows[i]).grid(row=i+1, column=0, sticky="w")
            self.info.insert(i, StringVar())
            self.info[i].set(self.item[i+1])
            Entry(self.janela_editar, textvariable=self.info[i]).grid(row=i+1, column=1, sticky="w")
        Button(self.janela_editar, width=10, text='Editar', command=self.editar).grid(row=10, column=0)
        Button(self.janela_editar, width=10, text='Cancelar', command=self.cancelar).grid(row=10, column=1)

    def editar(self):
        for i in range(len(self.info)):
            item = self.info[i].get()
            DB_R.editar_reservas(DB_R.pegar_colunas()[0], self.item[0], DB_R.pegar_colunas()[i+1], item)
        self.app.atualizar_arvore()
        self.janela_editar.destroy()

    def cancelar(self):
        self.janela_editar.destroy()

    def grab(self):
        self.janela_editar.grab_set()


#           OUTROS


class janela_erro():
    def __init__(self, janela, mensagem, app):
        self.app = app
        self.msg = mensagem
        self.janela_erro = janela
        self.janela_erro.grab_set()
        self.janela_erro.title("Deu ruim!")
        Frame(self.janela_erro, width=5, bd=1).grid(row=0, column=0, rowspan=1, padx=5, pady=5)
        Frame(self.janela_erro, width=5, bd=1).grid(row=0, column=2, rowspan=1, padx=5, pady=5)
        Frame(self.janela_erro, height=5, bd=1).grid(row=0, column=1, rowspan=1, padx=5, pady=5)
        Frame(self.janela_erro, height=5, bd=1).grid(row=2, column=1, rowspan=1, padx=5, pady=5)
        Frame(self.janela_erro, height=5, bd=1).grid(row=4, column=1, rowspan=1, padx=5, pady=5)
        Label(self.janela_erro, text=self.msg).grid(row=1, column=1, columnspan=1)
        Button(self.janela_erro, width=10, text='Ok', command=self.fechar).grid(row=3, column=1)

    def fechar(self):
        self.app.grab()
        self.janela_erro.destroy()


class janela_confirm():
    def __init__(self, janela, mensagem, index, app):
        self.app = app
        self.msg = mensagem
        self.index = index
        self.janela_confirm = janela
        self.janela_confirm.grab_set()
        self.janela_confirm.title("Tem certeza?")
        Frame(self.janela_confirm, width=5, bd=1).grid(row=0, column=0, rowspan=1, padx=5, pady=5)
        Frame(self.janela_confirm, width=5, bd=1).grid(row=0, column=3, rowspan=1, padx=5, pady=5)
        Frame(self.janela_confirm, height=5, bd=1).grid(row=0, column=1, rowspan=1, padx=5, pady=5)
        Frame(self.janela_confirm, height=5, bd=1).grid(row=2, column=1, rowspan=1, padx=5, pady=5)
        Frame(self.janela_confirm, height=5, bd=1).grid(row=4, column=1, rowspan=1, padx=5, pady=5)
        Label(self.janela_confirm, text=self.msg).grid(row=1, column=1, columnspan=2)
        Button(self.janela_confirm, width=10, text='Não', command=self.nao).grid(row=3, column=1)
        Button(self.janela_confirm, width=10, text='Sim', command=self.sim).grid(row=3, column=2)

    def nao(self):
        self.app.grab()
        self.janela_confirm.destroy()

    def sim(self):
        self.app.grab()
        self.janela_confirm.destroy()
        if self.index == 1:
            self.app.limpar_1()
        if self.index == 2:
            self.app.limpar_2()
        if self.index == 3:
            self.app.limpar_3()
            self.app.atualizar_arvore()

gui = interface_geral()