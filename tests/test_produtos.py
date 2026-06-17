import pytest


def test_listar_produtos_vazio(client):
    response = client.get("/produtos")

    assert response.status_code == 200
    assert response.json() == []


def test_criar_produto(client):
    response = client.post(
        "/produtos",
        json={
            "nome": "Teclado",
            "preco": 100.0,
            "estoque": 5,
            "ativo": True,
        },
    )

    data = response.json()

    assert response.status_code == 201
    assert data["id"] is not None
    assert data["nome"] == "Teclado"
    assert data["preco"] == 100.0


def test_persistencia_produto(client):
    client.post(
        "/produtos",
        json={
            "nome": "Mouse",
            "preco": 50.0,
        },
    )

    response = client.get("/produtos")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_produto_aparece_na_listagem(client):
    client.post(
        "/produtos",
        json={
            "nome": "Monitor",
            "preco": 800.0,
        },
    )

    response = client.get("/produtos")
    nomes = [produto["nome"] for produto in response.json()]

    assert "Monitor" in nomes


def test_buscar_produto_existente(client, produto_existente):
    response = client.get(f"/produtos/{produto_existente['id']}")

    assert response.status_code == 200
    assert response.json()["nome"] == "Notebook"


def test_buscar_produto_inexistente(client):
    response = client.get("/produtos/9999")

    assert response.status_code == 404


def test_deletar_produto(client, produto_existente):
    response = client.delete(f"/produtos/{produto_existente['id']}")

    assert response.status_code == 204


def test_confirmar_remocao(client, produto_existente):
    client.delete(f"/produtos/{produto_existente['id']}")

    response = client.get(f"/produtos/{produto_existente['id']}")

    assert response.status_code == 404


def test_deletar_produto_inexistente(client):
    response = client.delete("/produtos/9999")

    assert response.status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"nome": "", "preco": 100},
        {"nome": "Produto", "preco": -10},
        {"nome": "Produto", "preco": 0},
        {"nome": "", "preco": -5},
    ],
)
def test_payloads_invalidos_retorna_422(client, payload):
    response = client.post("/produtos", json=payload)

    assert response.status_code == 422


def test_isolamento_do_banco(client):
    response = client.get("/produtos")

    assert response.status_code == 200
    assert response.json() == []