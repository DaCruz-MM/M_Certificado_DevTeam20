import os.path as path
import csv

rows = [    # Numero de indentificação.
        'id',
            # Descrição da ferramenta
        'desc_ferramenta',
            # Fabricante
        'fabricante',
            # Voltagem de uso
        'volt_uso',
            # Part Number
        'p_num',
            # Tamanho
        'tamanho',
            # Unidade de medida
        'unidade_medida',
            # Tipo de ferramenta
        'tipo_ferramenta',
            # Material da ferramenta
        'material_ferramenta',
            # Tempo máximo de reserva
        'tempo_maximo']


if not path.exists('Ferramentas.csv'):
    with open('Ferramentas.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(rows)
        file.close()


def limpar_ferramentas():
    with open('Ferramentas.csv', 'w') as file_l:
        writer_l = csv.writer(file_l)
        writer_l.writerow(rows)
        file_l.close()


def reescrever_ferramenta(lista_r):
    with open('Ferramentas.csv', 'w') as file_r:
        writer_r = csv.writer(file_r)
        writer_r.writerow(rows)
        for row_r in lista_r:
            writer_r.writerow(row_r)
        file_r.close()


def gerar_id(new_n_i):
    with open('Ferramentas.csv', 'r') as file_i:
        reader_i = csv.DictReader(file_i)
        ver_i = 1
        n_i = 1
        if new_n_i:
            n_i = new_n_i
        for linha_i in reader_i:
            id_i = int(linha_i[rows[0]])
            if id_i == n_i:
                ver_i = 0
        if ver_i == 1:
            return n_i
        else:
            return gerar_id(n_i+1)


def ordenar_ferramentas():
    lista_s = []
    with open('Ferramentas.csv', 'r') as file_s:
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
        reescrever_ferramenta(lista_s)


def adicionar_ferramenta(f):
    with open('Ferramentas.csv', 'a') as file_b:
        if f[8]:
            writer_b = csv.DictWriter(file_b, fieldnames=rows)
            writer_b.writerow({rows[0]: gerar_id(1),
                               rows[1]: f[0],
                               rows[2]: f[1],
                               rows[3]: f[2],
                               rows[4]: f[3],
                               rows[5]: f[4],
                               rows[6]: f[5],
                               rows[7]: f[6],
                               rows[8]: f[7],
                               rows[9]: f[8]
                               })
            file_b.close()
            ordenar_ferramentas()


def remover_ferramenta(coluna, info):
    nova_lista = []
    with open('Ferramentas.csv', 'r') as file_c:
        reader_c = csv.DictReader(file_c)
        for row_c in reader_c:
            if int(row_c[coluna]) != int(info):
                nova_lista.append(list(row_c.values()))
        file_c.close()
        reescrever_ferramenta(nova_lista)


def selecionar_ferramenta(coluna, valor):
    lista_f = []
    with open('Ferramentas.csv', 'r') as file_f:
        reader_f = csv.DictReader(file_f)
        for row_f in reader_f:
            if row_f[coluna] == str(valor):
                lista_f.append(list(row_f.values()))
        file_f.close()
        return lista_f


def editar_ferramenta(coluna_f, valor_f, coluna_e, valor_e):
    lista_e = []
    with open('Ferramentas.csv', 'r') as file_e:
        reader_e = csv.DictReader(file_e)
        for row_e in reader_e:
            if row_e[coluna_f] == str(valor_f):
                row_e[coluna_e] = valor_e
                lista_e.append(list(row_e.values()))
            else:
                lista_e.append(list(row_e.values()))
        reescrever_ferramenta(lista_e)
        file_e.close()


def pegar_ferramentas():
    lista_p = []
    with open('Ferramentas.csv', 'r') as file_p:
        vetor = csv.DictReader(file_p)
        for i in vetor:
            i = list(i.values())
            lista_p.append(i)
        return lista_p


def pegar_colunas():
    return rows
