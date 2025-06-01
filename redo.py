import psycopg2
import json
from dotenv import load_dotenv
import os

load_dotenv()


def run_redo():
    # Conectar ao banco
    conn = psycopg2.connect(
        dbname=os.getenv('DATABASE_NAME'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
    )

    cursor = conn.cursor()

    # Caso a tabela ainda esteja presente, remove (ela foi perdida pois estava na memória)
    cursor.execute("DROP TABLE IF EXISTS dados;")

    # Cria a tabela nova (ela foi perdida pois estava na memória)
    cursor.execute(
        """
        CREATE TABLE dados (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(50),
            valor INTEGER
        );
    """
    )

    # Identificar transações commitadas
    cursor.execute(
        """
          WITH comecou AS (SELECT DISTINCT transacao_id FROM log_operacoes WHERE operacao = 'BEGIN' ORDER BY transacao_id),
          terminou AS (SELECT DISTINCT transacao_id FROM log_operacoes WHERE operacao = 'COMMIT' ORDER BY transacao_id),
          todas AS (SELECT DISTINCT transacao_id FROM log_operacoes ORDER BY transacao_id)	
          select * from ((select * from comecou intersect select * from terminou) union (select * from todas except select * from comecou)) order by transacao_id;
    """
    )
    committed_txns = [row[0] for row in cursor.fetchall()]
    print(f"Transações para REDO: {committed_txns}")

    # Aplicar REDO para cada transação
    for txn_id in committed_txns:
        cursor.execute(
            """
            SELECT operacao, tabela, id_registro, dados_novos
            FROM log_operacoes 
            WHERE transacao_id = %s
            AND operacao NOT IN ('BEGIN', 'COMMIT')
            ORDER BY id
        """,
            (txn_id,),
        )

        for op in cursor.fetchall():
            operacao, tabela, id_registro, dados = op

            if operacao == 'INSERT':
                cols = ', '.join(dados.keys())
                vals = ', '.join([f"'{str(v)}'" for v in dados.values()])
                query = f"INSERT INTO {tabela} ({cols}) VALUES ({vals})"
                cursor.execute(query)
                print(f"Redo: Transação {txn_id} - INSERT no registro {id_registro}")

            elif operacao == 'UPDATE':
                sets = ', '.join([f"{k} = '{str(v)}'" for k, v in dados.items()])
                query = f"UPDATE {tabela} SET {sets} WHERE id = {id_registro}"
                cursor.execute(query)
                print(f"Redo: Transação {txn_id} - UPDATE no registro {id_registro}")

            elif operacao == 'DELETE':
                query = f"DELETE FROM {tabela} WHERE id = {id_registro}"
                cursor.execute(query)
                print(f"Redo: Transação {txn_id} - DELETE no registro {id_registro}")

            conn.commit()

    # Cria novamente os triggers da tabela dados que foi perdido

    cursor.execute(
        """
      CREATE OR REPLACE TRIGGER trg_log_delete
      BEFORE DELETE ON dados
      FOR EACH ROW EXECUTE FUNCTION log_delete();
      """
    )
    cursor.execute(
        """
      CREATE OR REPLACE TRIGGER trg_log_update
      BEFORE UPDATE ON dados
      FOR EACH ROW EXECUTE FUNCTION log_update();
      """
    )
    cursor.execute(
        """
      CREATE OR REPLACE TRIGGER trg_log_insert
      BEFORE INSERT ON dados
      FOR EACH ROW EXECUTE FUNCTION log_insert();
      """
    )

    print("Triggers recriados com sucesso.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    run_redo()
