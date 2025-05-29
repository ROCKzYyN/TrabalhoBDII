import json

def create_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS alunos;')

    cursor.execute('''
        CREATE TABLE 
            mat integer NOT NULL,
            nome VARCHAR(100) NOT NULL,
            idade INT NOT NULL,
        );
    ''')

def populando_table(cursor):
    create_table(cursor)

    file = open('Dados/dados.json', 'r')

    try:
        data = json.load(file)['INITIAL']
        tuples = list( zip(data['mat'], data['nome'], data['idade']) )

        for tupla in tuples:
            tupla = [str(column) for column in tupla]

            values = ', '.join(tupla)

            insert_query = 'INSERT INTO alunos (mat, nome, idade) VALUES (' + values + ');'
            cursor.execute(insert_query)
    
    finally:
        file.close() #tabela populada com sucesso
