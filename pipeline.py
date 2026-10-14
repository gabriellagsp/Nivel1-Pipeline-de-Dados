# criação do Pipeline

import csv
import sqlite3

#abrir o arquivo CSV com os dados de produção de alimentos
with open ('producao_alimentos.csv', 'r', encoding = 'utf-8') as file:
    
    #criar um leitor de CSV
    reader = csv.reader(file)

    #pular a primeira linha do csv
    next(reader)

    # CRIAR UMA CONEXÃO COM O BANCO DE DADOS
    conn = sqlite3.connect('eng_eba.db')

    #Iserir lógica caso a tabela já exista
    conn.execute('DROP TABLE IF EXISTS producao')

    #criar tabela novamente
    conn.execute('''CREATE TABLE producao (
            produto TEXT,
            quantidade REAL,
            preco_medio REAL,
            receita_total REAL,
            custo_kg REAL,
            margem_lucro_porcentagem REAL
            )
''')

    # INSERIR OS DADOS DO CSV NO BANCO DE DADOS
    for row in reader:
        if float(row[1]) > float(10):
            margem_lucro_porcentagem = (float(row[3]) - float(row[1])*float(row[4])) / float(row[3])*100  
                    
            conn.execute('INSERT INTO producao (produto, quantidade, preco_medio, receita_total, custo_kg, margem_lucro_porcentagem) VALUES (?,?,?,?,?,?)', (row[0], row[1], row[2], row[3], row[4], margem_lucro_porcentagem))  
    
    conn.commit()
    conn.close()

print('Pipeline concluído com sucesso')

# Inserida para visualização
def verificar_tabela (banco_dados, tabela):
    conn = sqlite3.connect(banco_dados)

    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {tabela}')
    resultados = cursor.fetchall()
    
    return resultados

dados = verificar_tabela('eng_eba.db', 'producao')
for i in dados:
    print (i)
