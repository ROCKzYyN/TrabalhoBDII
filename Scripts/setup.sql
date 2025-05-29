-- configurando tabelas e triggers
-- Tabela em memória (UNLOGGED)
CREATE UNLOGGED TABLE dados (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50),
    valor INTEGER
);

-- Tabela de log
CREATE TABLE log_operacoes (
    id SERIAL PRIMARY KEY,
    transacao_id INTEGER NOT NULL,
    operacao VARCHAR(10) NOT NULL,
    tabela VARCHAR(50) NOT NULL,
    id_registro INTEGER,
    dados_antigos JSONB,
    dados_novos JSONB,
    tipo_log VARCHAR(10) NOT NULL CHECK (tipo_log IN ('OPERACAO', 'COMMIT')),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Triggers para registrar operações de INSERT, UPDATE e DELETE

-- Trigger para INSERT
CREATE OR REPLACE FUNCTION log_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO log_operacoes (transacao_id, operacao, tabela, id_registro, dados_novos, tipo_log)
    VALUES (txid_current(), 'INSERT', TG_TABLE_NAME, NEW.id, row_to_json(NEW), 'OPERACAO');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_insert
AFTER INSERT ON dados
FOR EACH ROW EXECUTE FUNCTION log_insert();

-- Trigger para UPDATE
CREATE OR REPLACE FUNCTION log_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO log_operacoes (transacao_id, operacao, tabela, id_registro, dados_antigos, dados_novos, tipo_log)
    VALUES (txid_current(), 'UPDATE', TG_TABLE_NAME, NEW.id, row_to_json(OLD), row_to_json(NEW), 'OPERACAO');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_update
AFTER UPDATE ON dados
FOR EACH ROW EXECUTE FUNCTION log_update();

-- Trigger para DELETE
CREATE OR REPLACE FUNCTION log_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO log_operacoes (transacao_id, operacao, tabela, id_registro, dados_antigos, tipo_log)
    VALUES (txid_current(), 'DELETE', TG_TABLE_NAME, OLD.id, row_to_json(OLD), 'OPERACAO');
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_delete
AFTER DELETE ON dados
FOR EACH ROW EXECUTE FUNCTION log_delete();