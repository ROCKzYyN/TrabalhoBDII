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