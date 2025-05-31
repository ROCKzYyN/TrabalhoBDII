-- exemplo de transações com o banco de dados
-- Transação 1
BEGIN;
INSERT INTO log_operacoes (transacao_id, operacao) VALUES (txid_current(), 'BEGIN');
INSERT INTO dados (nome, valor) VALUES ('Item1', 100);
INSERT INTO dados (nome, valor) VALUES ('Item2', 200);
INSERT INTO log_operacoes (transacao_id, operacao) VALUES (txid_current(), 'COMMIT');
COMMIT;

-- Transação 2
BEGIN;
INSERT INTO log_operacoes (transacao_id, operacao) VALUES (txid_current(), 'BEGIN');
UPDATE dados SET valor = 150 WHERE nome = 'Item1';
DELETE FROM dados WHERE nome = 'Item2';
INSERT INTO log_operacoes (transacao_id, operacao) VALUES (txid_current(), 'COMMIT');
COMMIT;

-- Insert qualquer
INSERT INTO dados (nome, valor) VALUES ('Item3', 300);