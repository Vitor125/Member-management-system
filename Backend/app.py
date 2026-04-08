from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_CONFIG = {
    "dbname": "Teste Vitor",
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "postgres",
}


@app.get("/teste01")
def fake():
    return jsonify({
        "id": 1,
        "nome": "Produto Fake",
        "preco": 99.9
    })


@app.get("/membros_pg")
def membros_pg():
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT nome, nome_dos_responsaveis
                    FROM membros_pg
                    """
                )
                dados = cur.fetchall()

        return jsonify(dados)
    except Exception as exc:
        return jsonify({
            "erro": "Falha ao consultar membros.",
            "detalhe": str(exc)
        }), 500


@app.post("/membros_pg")
def criar_membro_pg():
    dados = request.get_json(silent=True) or request.form.to_dict()
    nome = (dados.get("nome") or "").strip()
    data_de_nascimento = (dados.get("data_de_nascimento") or "").strip()
    nome_dos_responsaveis = (dados.get("nome_dos_responsaveis") or "").strip()
    igreja_id = dados.get("igreja_id")

    if not nome or not data_de_nascimento or not nome_dos_responsaveis or igreja_id is None:
        return jsonify({
            "erro": "Os campos 'nome', 'data_de_nascimento', 'nome_dos_responsaveis' e 'igreja_id' sao obrigatorios."
        }), 400

    try:
        igreja_id = int(igreja_id)
    except (TypeError, ValueError):
        return jsonify({
            "erro": "O campo 'igreja_id' precisa ser numerico."
        }), 400

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO membros_pg (nome, data_de_nascimento, nome_dos_responsaveis, igreja_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, nome, data_de_nascimento, nome_dos_responsaveis, igreja_id
                    """,
                    (nome, data_de_nascimento, nome_dos_responsaveis, igreja_id)
                )
                registro = cur.fetchone()

        return jsonify({
            "mensagem": "Membro criado com sucesso.",
            "registro": registro
        }), 201
    except Exception as exc:
        return jsonify({
            "erro": "Falha ao inserir membro.",
            "detalhe": str(exc)
        }), 500
