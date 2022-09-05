import os.path as path
import csv

rows = ['ID',                       # Numero de indentificação.
        'ferramenta',  # Código da ferramenta
        'desc_solicitacao',               # Descrição da solicitação
        'data_retirada',          # Data e hora da retirada
        'data_devolucao',              # Data e hora prevista de devolução
        'tecnico',]                 # Técnico responsável pela retirada (nome completo)


# Cria o arquivo caso não exista.
if not path.exists('Reservas.csv'):
    with open('Reservas.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(rows)
        file.close()


# Reescreve todo arquivo, porem não salva nenhuma ferramenta, então basicamente deixa "zerada".
def limpar_reservas():
    with open('Reservas.csv', 'w') as file_l:
        writer_l = csv.writer(file_l)
        writer_l.writerow(rows)
        file_l.close()


# Reescreve todo arquivo a partir de uma lista.
def reescrever_reservas(lista_r):
    with open('Reservas.csv', 'w') as file_r:
        writer_r = csv.writer(file_r)
        writer_r.writerow(rows)
        for row_r in lista_r:
            writer_r.writerow(row_r)
        file_r.close()


# Obtem o menor numero de ID que não esteja sendo utilizado
def gerar_id(new_n_i):
    with open('Reservas.csv', 'r') as file_i:
        reader_i = csv.DictReader(file_i)
        ver_i = 1
        n_i = 1
        if new_n_i:
            n_i = new_n_i
        for linha_i in reader_i:
            id_i = int(linha_i['ID'])
            if id_i == n_i:
                ver_i = 0
        if ver_i == 1:
            return n_i
        else:
            return gerar_id(n_i+1)


# Reorganiza os funcionarios de acordo com o ID, do menor para o maior.
def ordenar_reservas():
    lista_s = []
    with open('Reservas.csv', 'r') as file_s:
        vetor = csv.DictReader(file_s)
        for i in vetor:
            i = list(i.values())
            lista_s.append(i)
        file_s.close()
        for i in range(len(lista_s)):
            for j in range(i + 1, len(lista_s)):
                if lista_s[i][0] > lista_s[j][0]:
                    temp = lista_s[i]
                    lista_s[i] = lista_s[j]
                    lista_s[j] = temp
        reescrever_reservas(lista_s)


# Adiciona um no funcionario a partir de uma lista com as informações.
def adicionar_reservas(f):
    with open('Reservas.csv', 'a') as file_b:
        if f[4]:
            writer_b = csv.DictWriter(file_b, fieldnames=rows)
            writer_b.writerow({rows[0]: gerar_id(1),
                               rows[1]: f[0],
                               rows[2]: f[1],
                               rows[3]: f[2],
                               rows[4]: f[3],
                               rows[5]: f[4],
                               })
            file_b.close()
            ordenar_reservas()


# Remove um funcionario de acordo com as informações passadas como parametro.
def remover_reservas(coluna, info):
    nova_lista = []
    with open('Reservas.csv', 'r') as file_c:
        reader_c = csv.DictReader(file_c)
        for row_c in reader_c:
            if int(row_c[coluna]) != int(info):
                nova_lista.append(list(row_c.values()))
        file_c.close()
        reescrever_reservas(nova_lista)


# Retorna um funcionario de acordo com as informações passadas como parametro.
def selecionar_reservas(coluna, valor):
    lista_f = []
    with open('Reservas.csv', 'r') as file_f:
        reader_f = csv.DictReader(file_f)
        for row_f in reader_f:
            if row_f[coluna] == str(valor):
                lista_f.append(list(row_f.values()))
        file_f.close()
        return lista_f


# Edita um funcionarios de acordo com as informações passadas como parametro.
def editar_reservas(coluna_f, valor_f, coluna_e, valor_e):
    lista_e = []
    with open('Reservas.csv', 'r') as file_e:
        reader_e = csv.DictReader(file_e)
        for row_e in reader_e:
            if row_e[coluna_f] == str(valor_f):
                row_e[coluna_e] = valor_e
                lista_e.append(list(row_e.values()))
            else:
                lista_e.append(list(row_e.values()))
        reescrever_reservas(lista_e)
        file_e.close()


# Retorna uma lista com todos os funcionarios do arquivo.
def pegar_reservas():
    lista_p = []
    with open('Reservas.csv', 'r') as file_p:
        vetor = csv.DictReader(file_p)
        for i in vetor:
            i = list(i.values())
            lista_p.append(i)
        return lista_p


def pegar_colunas():
    return rows
