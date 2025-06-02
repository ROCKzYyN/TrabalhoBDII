<div align="center">
  <h1 align="center">TrabalhoBDII</h1>

  <p align="center">
   Implementação de um mecanismo de log Redo usando o SGBD.
    <br />
  </p>
</div>

## 💡 Descrição
Alunos: João Vithor Knakievicz e Wictor Greselli
É um projeto da disciplina de Banco de Dados II que tem como objetivo implementar um mecanismo de logging e recuperação de dados para tabelas temporárias (`UNLOGGED`) no PostgreSQL. O sistema utiliza triggers para registrar operações em uma tabela de log e um script em Python (`redo.py`) para recuperar os dados perdidos após uma queda do sistema.
---

## ⚙️ Como Executar

### 1. Iniciar o PostgreSQL

```bash
sudo service postgresql start
```

### 2. Configurar o Banco

```bash
psql -U seu_user -d seu_banco -f setup.sql
```

### 3. Executar Transações

```bash
psql -U seu_user -d seu_banco -f transacoes.sql
```

### 4. Simular Queda do SGBD

```bash
sudo kill -9 $(pidof postgres)
```

### 5. Reiniciar o PostgreSQL

```bash
sudo service postgresql start
```

### 6. Executar o Script de REDO

Crie um arquivo `.env` com os dados do seu banco:

```
DATABASE_NAME=seu_banco
DATABASE_USER=seu_user
DATABASE_PASSWORD=sua_senha
DATABASE_HOST=localhost
```

Execute o script:

```bash
python3 redo.py
```

---

## ✅ Saída Esperada do Script REDO

```text
Transações para REDO: [12345, 12346]
Redo: Transação 12345 - INSERT no registro 1
Redo: Transação 12345 - INSERT no registro 2
Redo: Transação 12346 - UPDATE no registro 1
Redo: Transação 12346 - DELETE no registro 2
Triggers recriados com sucesso.
```

---

## 🧪 Exemplo de Transações (`transacoes.sql`)

```sql
INSERT INTO dados (nome, valor) VALUES ('Produto A', 100);
INSERT INTO dados (nome, valor) VALUES ('Produto B', 200);
UPDATE dados SET valor = 150 WHERE nome = 'Produto A';
DELETE FROM dados WHERE nome = 'Produto B';
```

Após a execução do `redo.py`, o estado final da tabela será:

```sql
SELECT * FROM dados;
```

Resultado:

```
 id |   nome    | valor
----+-----------+-------
  1 | Produto A |   150
```

---

## 🧰 Dependências utilizadas

- PostgreSQL
- Python 3.8+
---

> Projeto para a disciplina de Banco de Dados II.
