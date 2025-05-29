-- exemplo de transações com o banco de dados
-- Transação 1
BEGIN;
INSERT INTO dados (nome, valor) VALUES ('Item1', 100);
INSERT INTO dados (nome, valor) VALUES ('Item2', 200);
INSERT INTO log_operacoes (transacao_id, tipo_log) VALUES (txid_current(), 'COMMIT');
COMMIT;

-- Transação 2
BEGIN;
UPDATE dados SET valor = 150 WHERE nome = 'Item1';
DELETE FROM dados WHERE nome = 'Item2';
INSERT INTO log_operacoes (transacao_id, tipo_log) VALUES (txid_current(), 'COMMIT');
COMMIT;