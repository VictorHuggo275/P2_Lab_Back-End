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
|---|---|---|
| id | Integer | Chave primária gerada automaticamente pelo banco |
| nome | String | Nome do produto |
| preco | Float | Preço em reais |
| estoque | Integer | Quantidade em estoque |
| ativo | Boolean | Disponível para venda |

---

# Endpoints

## Listar Produtos

```http
GET /produtos
```

Retorna todos os produtos cadastrados.

---

## Criar Produto

```http
POST /produtos
```

Exemplo:

```json
{
  "nome": "Notebook",
  "preco": 3500,
  "estoque": 10,
  "ativo": true
}
```

---

## Buscar Produto por ID

```http
GET /produtos/{id}
```

Retorna o produto informado ou erro 404 caso não exista.

---

## Deletar Produto

```http
DELETE /produtos/{id}
```

Remove o produto informado ou retorna erro 404 caso não exista.

---

# Configuração do Banco de Dados

O projeto utiliza dois bancos PostgreSQL separados:

| Serviço | Porta | Finalidade |
|---|---|---|
| db | 5432 | Desenvolvimento |
| db_test | 5433 | Testes automatizados |

O banco de testes é separado do banco principal para garantir isolamento durante a execução dos testes.

---

# Instalação

Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

---

# Executando o Banco de Testes

Inicie o banco PostgreSQL utilizado pelos testes:

```bash
docker-compose up -d db_test
```

Verifique se o container está rodando:

```bash
docker ps
```

---

# Executando a API

Suba todos os serviços:

```bash
docker-compose up -d
```

A API estará disponível em:

```text
http://localhost:8000
```

Documentação Swagger:

```text
http://localhost:8000/docs
```

---

# Executando os Testes

Com o banco de testes ativo, execute:

```bash
pytest --cov=main -v
```

---

# Casos de Teste Implementados

A suíte de testes cobre:

- Listar produtos com banco vazio
- Criar produto e verificar persistência
- Criar produto e verificar presença na listagem
- Buscar produto existente por ID
- Buscar produto inexistente (404)
- Deletar produto (204)
- Confirmar remoção após DELETE
- Deletar produto inexistente (404)
- Validação de payload inválido com retorno 422
- Isolamento do banco entre execuções

Total: **14 testes automatizados**

---

# Fixtures de Teste

A fixture `client` é responsável pelo isolamento dos testes.

Antes de cada teste, as tabelas são criadas utilizando:

```python
Base.metadata.create_all(bind=engine)
```

A dependência do banco é substituída utilizando:

```python
app.dependency_overrides[get_db]
```

Dessa forma, todos os testes utilizam exclusivamente o banco PostgreSQL de teste (`db_test`).

Após a execução, as tabelas são removidas utilizando:

```python
Base.metadata.drop_all(bind=engine)
```

Cada teste inicia com um banco limpo, evitando compartilhamento de dados entre execuções e garantindo independência da ordem dos testes.

Também existe a fixture auxiliar `produto_existente`, que depende da fixture `client` e cria produtos previamente cadastrados para testes que necessitam de dados existentes.

---

# Saída Esperada

```text
============================= test session starts =============================

collected 14 items

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
...
tests/test_produtos.py::test_isolamento_do_banco PASSED

================================ tests coverage ================================

Name      Stmts   Miss  Cover
-----------------------------
main.py      60      4    93%
-----------------------------
TOTAL        60      4    93%

============================== 14 passed in 0.80s ==============================
```

---

# Comando de Verificação Final

Para verificar o funcionamento completo do projeto:

```bash
docker-compose up -d db_test && pytest --cov=main -v
```

Todos os testes devem passar com cobertura superior a 85%.