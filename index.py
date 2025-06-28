from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'dados.txt')

@app.route('/namid', methods=['GET'])
def search_by_name():
    search_term = request.args.get('name')
    if not search_term:
        return jsonify({"error": "Parâmetro 'name' é obrigatório"}), 400

    try:
        if not os.path.exists(DATA_FILE):
            return jsonify({"error": "Arquivo de dados não encontrado"}), 404

        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)

        results = [
            {"id": item["id"], "name": item["name"]}
            for item in data
            if "name" in item and search_term.lower() in item["name"].lower()
        ]

        return jsonify(results)

    except json.JSONDecodeError:
        return jsonify({"error": "Formato inválido no arquivo de dados"}), 500
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

# WSGI handler para a Vercel
def handler(environ, start_response):
    from werkzeug.middleware.dispatcher import DispatcherMiddleware
    from werkzeug.serving import run_simple
    return DispatcherMiddleware(app)(environ, start_response)
