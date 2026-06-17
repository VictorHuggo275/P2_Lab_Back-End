# API de Produtos - FastAPI + PostgreSQL

## Subindo o banco de teste

```bash
docker-compose up -d db_test
```

Verifique se o container está healthy:

```bash
docker ps
```

## Executando os testes

```bash
pytest -v
```

Ou com cobertura:

```bash
pytest --cov=main --cov-report=term-missing -v
```

## Saída esperada

Exemplo:

```text
================= test session starts =================
...
11 passed
================= 11 passed =================
```

## Isolamento entre testes

O projeto utiliza uma fixture `client` com `yield`.

Antes de cada teste:
- cria as tabelas com `Base.metadata.create_all()`;
- substitui a dependência `get_db` usando `app.dependency_overrides`.

Após cada teste:
- remove todas as tabelas com `Base.metadata.drop_all()`.

Dessa forma cada teste executa em um banco limpo, independente da ordem de execução.
