CREATE UNLOGGED TABLE aluno (
    matricula VARCHAR(10) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INT NOT NULL,
    email VARCHAR(100) NOT NULL,
);
 
CREATE TABLE log_aluno (
    log_id SERIAL PRIMARY KEY,
    matricula VARCHAR(10),
    operacao VARCHAR(10),
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);