from flask import Flask, request, jsonify
import json
import os
import re

app = Flask(__name__)

# Caminho para o arquivo de dados (ajuste conforme necessário)
DATA_FILE = 'api/dados.txt'

@app.route('/namid', methods=['GET'])
def search_by_name():
    # Obtém o parâmetro 'name' da query string
    search_term = request.args.get('name')

    if not search_term:
        return jsonify({"error": "Parâmetro 'name' é obrigatório"}), 400

    try:
        # Verifica se o arquivo existe
        if not os.path.exists(DATA_FILE):
            return jsonify({"error": "Arquivo de dados não encontrado"}), 404

        # Lê e parseia o arquivo JSON
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Filtra os itens usando expressão regular para match exato da palavra
        results = [
            {"id": item["id"], "name": item["name"]}
            for item in data
            if "name" in item and re.search(rf'\b{re.escape(search_term)}\b', item["name"], flags=re.IGNORECASE)
        ]

        return jsonify(results)

    except json.JSONDecodeError:
        return jsonify({"error": "Formato inválido no arquivo de dados"}), 500
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

def vercel_handler(request):
    with app.app_context():
        response = app.full_dispatch_request()
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data(as_text=True)
        }
