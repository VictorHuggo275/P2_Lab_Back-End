import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, Base, get_db

# Banco de TESTE (fixo na porta 5433)
DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/produtos_test"

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture
def client():
    # Cria as tabelas antes dos testes
    Base.metadata.create_all(bind=engine)

    # Sobrescreve a dependência do banco
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Limpeza após os testes
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def produto_existente(client):
    response = client.post(
        "/produtos",
        json={
            "nome": "Notebook",
            "preco": 3500,
            "estoque": 10,
            "ativo": True,
        },
    )
    return response.json()