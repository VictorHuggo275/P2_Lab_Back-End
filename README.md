# API de Produtos - FastAPI + PostgreSQL + Pytest

Projeto desenvolvido para a disciplina **Desenvolvimento de APIs com FastAPI**, com o objetivo de implementar uma API REST para gerenciamento de produtos utilizando FastAPI, SQLAlchemy, PostgreSQL e testes automatizados com Pytest.

---

## Tecnologias Utilizadas

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pytest
- Docker
- Docker Compose

---

## Estrutura do Projeto

```text
.
├── main.py
├── conftest.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── README.md
└── tests
    ├── __init__.py
    └── test_produtos.py
```

---

## Modelo de Dados

### Produto

| Campo | Tipo | Descrição |
|---------|---------|---------|
| id | Integer | Chave primária gerada automaticamente |
| nome | String | Nome do produto |
| preco | Float | Preço do produto |
| estoque | Integer | Quantidade em estoque |
| ativo | Boolean | Disponível para venda |

---

## Endpoints

### Listar Produtos

```http
GET /produtos
```

Resposta:

```json
[
  {
    "id": 1,
    "nome": "Notebook",
    "preco": 3500.0,
    "estoque": 10,
    "ativo": true
  }
]
```

---

### Criar Produto

```http
POST /produtos
```

Exemplo de requisição:

```json
{
  "nome": "Notebook",
  "preco": 3500,
  "estoque": 10,
  "ativo": true
}
```

Resposta:

```json
{
  "id": 1,
  "nome": "Notebook",
  "preco": 3500,
  "estoque": 10,
  "ativo": true
}
```

---

### Buscar Produto por ID

```http
GET /produtos/{id}
```

Resposta:

```json
{
  "id": 1,
  "nome": "Notebook",
  "preco": 3500,
  "estoque": 10,
  "ativo": true
}
```

---

### Deletar Produto

```http
DELETE /produtos/{id}
```

Resposta:

```http
204 No Content
```

---

# Configuração do Banco de Dados

O projeto utiliza dois bancos PostgreSQL separados:

| Serviço | Porta | Finalidade |
|----------|----------|----------|
| db | 5432 | Desenvolvimento |
| db_test | 5433 | Testes Automatizados |

---

## Subindo o Banco de Testes

Executar:

```bash
docker compose up -d db_test
```

Verificar se o container está rodando:

```bash
docker ps
```

Saída esperada:

```text
produtos_db_test
```

Verificar saúde do banco:

```bash
docker inspect produtos_db_test
```

Deve aparecer:

```json
"Status": "healthy"
```

---

## Executando a API

Subir o banco principal:

```bash
docker compose up -d db
```

Executar a aplicação:

```bash
uvicorn main:app --reload
```

A documentação Swagger estará disponível em:

```text
http://localhost:8000/docs
```

---

## Executando os Testes

### Com Python Local

```bash
pytest -v
```

---

### Com Cobertura

```bash
pytest --cov=main --cov-report=term-missing -v
```

---

### Utilizando Docker

Construir a imagem:

```bash
docker build -t produtos-api .
```

Executar os testes:

```bash
docker run --rm \
--network host \
-v $(pwd):/app \
-w /app \
produtos-api \
pytest --cov=main -v
```

---

## Casos de Teste Implementados

A suíte contém testes para:

- Listar produtos com banco vazio
- Criar produto
- Verificar persistência após criação
- Verificar presença na listagem
- Buscar produto existente por ID
- Buscar produto inexistente
- Deletar produto
- Confirmar remoção após DELETE
- Deletar produto inexistente
- Validação de payloads inválidos (422)
- Isolamento do banco entre execuções

Total: **11 testes automatizados**

---

## Exemplo de Saída Esperada

```text
============================= test session starts =============================

tests/test_produtos.py::test_listar_produtos_vazio PASSED
tests/test_produtos.py::test_criar_produto PASSED
tests/test_produtos.py::test_persistencia_produto PASSED
tests/test_produtos.py::test_produto_aparece_na_listagem PASSED
tests/test_produtos.py::test_buscar_produto_existente PASSED
tests/test_produtos.py::test_buscar_produto_inexistente PASSED
tests/test_produtos.py::test_deletar_produto PASSED
tests/test_produtos.py::test_confirmar_remocao PASSED
tests/test_produtos.py::test_deletar_produto_inexistente PASSED
tests/test_produtos.py::test_payloads_invalidos_retorna_422 PASSED
tests/test_produtos.py::test_isolamento_do_banco PASSED

============================= 11 passed =============================
```

---

## Como Funciona o Isolamento dos Testes

A fixture `client` implementa isolamento completo entre os testes:

1. Cria as tabelas antes da execução com:

```python
Base.metadata.create_all(bind=engine)
```

2. Substitui a dependência do banco utilizando:

```python
app.dependency_overrides[get_db]
```

3. Executa os testes utilizando o banco PostgreSQL de teste.

4. Remove todas as tabelas após a execução com:

```python
Base.metadata.drop_all(bind=engine)
```

Dessa forma cada execução inicia com um banco limpo, garantindo independência da ordem dos testes e evitando compartilhamento de estado.

---
