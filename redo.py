import psycopg2
import json
import os

def run_redo():
    # Conectar ao banco
    conn = psycopg2.connect(
        dbname="seu_banco",
        user="seu_user",
        password="sua_senha",
        host="localhost"
    )
    cursor = conn.cursor()
    
    # Identificar transações commitadas
    cursor.execute("""
        SELECT DISTINCT transacao_id 
        FROM log_operacoes 
        WHERE tipo_log = 'COMMIT'
        ORDER BY transacao_id
    """)
    committed_txns = [row[0] for row in cursor.fetchall()]
    print(f"Transações para REDO: {committed_txns}")

    # Aplicar REDO para cada transação
    for txn_id in committed_txns:
        cursor.execute("""
            SELECT operacao, tabela, id_registro, dados_novos 
            FROM log_operacoes 
            WHERE transacao_id = %s 
            AND tipo_log = 'OPERACAO'
            ORDER BY id
        """, (txn_id,))
        
        for op in cursor.fetchall():
            operacao, tabela, id_registro, dados_novos = op
            dados = json.loads(dados_novos) if dados_novos else {}
            
            if operacao == 'INSERT':
                cols = ', '.join(dados.keys())
                vals = ', '.join([f"'{str(v)}'" for v in dados.values()])
                query = f"INSERT INTO {tabela} ({cols}) VALUES ({vals})"
                print(f"Redo: Transação {txn_id} - INSERT no registro {id_registro}")
                
            elif operacao == 'UPDATE':
                sets = ', '.join([f"{k} = '{str(v)}'" for k, v in dados.items()])
                query = f"UPDATE {tabela} SET {sets} WHERE id = {id_registro}"
                print(f"Redo: Transação {txn_id} - UPDATE no registro {id_registro}")
                
            elif operacao == 'DELETE':
                query = f"DELETE FROM {tabela} WHERE id = {id_registro}"
                print(f"Redo: Transação {txn_id} - DELETE no registro {id_registro}")
                
            cursor.execute(query)
            conn.commit()

    # Atualizar sequências (evitar conflitos de IDs)
    cursor.execute("SELECT setval('dados_id_seq', (SELECT MAX(id) FROM dados))")
    conn.commit()
    cursor.close()
    conn.close()

if _name_ == "_main_":
    run_redo()