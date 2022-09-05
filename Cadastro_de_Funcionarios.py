import os.path as path
import csv

rows = ['ID',                       # Numero de indentificação.
        'Nome',  # Nome do funcionário
        'Cpf',               # cpf do funcionário
        'telefone',          # telefone
        'turno',              # turno de trabalho
        'grupo',]                 # Grupo


# Cria o arquivo caso não exista.
if not path.exists('Funcionarios.csv'):
    with open('Funcionarios.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(rows)
        file.close()

def cpf_validate(numbers):
    numbers = str(numbers)
    #  Obtém os números do CPF e ignora outros caracteres
    cpf = [int(char) for char in numbers if char.isdigit()]

    #  Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
    #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
    if cpf == cpf[::-1]:
        return False

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True

# Reescreve todo arquivo, porem não salva nenhuma ferramenta, então basicamente deixa "zerada".
def limpar_funcionarios():
    with open('Funcionarios.csv', 'w') as file_l:
        writer_l = csv.writer(file_l)
        writer_l.writerow(rows)
        file_l.close()


# Reescreve todo arquivo a partir de uma lista.
def reescrever_funcionarios(lista_r):
    with open('Funcionarios.csv', 'w') as file_r:
        writer_r = csv.writer(file_r)
        writer_r.writerow(rows)
        for row_r in lista_r:
            writer_r.writerow(row_r)
        file_r.close()


# Obtem o menor numero de ID que não esteja sendo utilizado
def gerar_id(new_n_i):
    with open('Funcionarios.csv', 'r') as file_i:
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
def ordenar_funcionarios():
    lista_s = []
    with open('Funcionarios.csv', 'r') as file_s:
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
        reescrever_funcionarios(lista_s)


# Adiciona um no funcionario a partir de uma lista com as informações.
def adicionar_funcionarios(f):
    with open('Funcionarios.csv', 'a') as file_b:
        if f[4] and cpf_validate(f[1]):
            writer_b = csv.DictWriter(file_b, fieldnames=rows)
            writer_b.writerow({rows[0]: gerar_id(1),
                               rows[1]: f[0],
                               rows[2]: f[1],
                               rows[3]: f[2],
                               rows[4]: f[3],
                               rows[5]: f[4],
                               })
            file_b.close()
            ordenar_funcionarios()


# Remove um funcionario de acordo com as informações passadas como parametro.
def remover_funcionarios(coluna, info):
    nova_lista = []
    with open('Funcionarios.csv', 'r') as file_c:
        reader_c = csv.DictReader(file_c)
        for row_c in reader_c:
            if int(row_c[coluna]) != int(info):
                nova_lista.append(list(row_c.values()))
        file_c.close()
        reescrever_funcionarios(nova_lista)


# Retorna um funcionario de acordo com as informações passadas como parametro.
def selecionar_funcionarios(coluna, valor):
    lista_f = []
    with open('Funcionarios.csv', 'r') as file_f:
        reader_f = csv.DictReader(file_f)
        for row_f in reader_f:
            if row_f[coluna] == str(valor):
                lista_f.append(list(row_f.values()))
        file_f.close()
        return lista_f


# Edita um funcionarios de acordo com as informações passadas como parametro.
def editar_funcionarios(coluna_f, valor_f, coluna_e, valor_e):
    lista_e = []
    with open('Funcionarios.csv', 'r') as file_e:
        reader_e = csv.DictReader(file_e)
        for row_e in reader_e:
            if row_e[coluna_f] == str(valor_f):
                row_e[coluna_e] = valor_e
                lista_e.append(list(row_e.values()))
            else:
                lista_e.append(list(row_e.values()))
        reescrever_funcionarios(lista_e)
        file_e.close()


# Retorna uma lista com todos os funcionarios do arquivo.
def pegar_funcionarios():
    lista_p = []
    with open('Funcionarios.csv', 'r') as file_p:
        vetor = csv.DictReader(file_p)
        for i in vetor:
            i = list(i.values())
            lista_p.append(i)
        return lista_p


def pegar_colunas():
    return rows
