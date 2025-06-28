from flask import Flask, request, jsonify
import json
import os
import re

app = Flask(__name__)

DATA_FILE = 'api/dados.txt'

@app.route('/namid', methods=['GET'])
def search_by_name():
    search_term = request.args.get('name')
    search_type = request.args.get('type', 'contains')  # padrão: contém o termo

    if not search_term:
        return jsonify({"error": "Parâmetro 'name' é obrigatório"}), 400

    try:
        if not os.path.exists(DATA_FILE):
            return jsonify({"error": "Arquivo de dados não encontrado"}), 404

        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)

        search_term_lower = search_term.lower()
        results = []

        for item in data:
            if "name" not in item:
                continue
                
            item_name_lower = item["name"].lower()
            
            if search_type == 'exact' and item_name_lower == search_term_lower:
                results.append({"id": item["id"], "name": item["name"]})
            elif search_type == 'start' and item_name_lower.startswith(search_term_lower):
                results.append({"id": item["id"], "name": item["name"]})
            elif search_type == 'word' and search_term_lower in item_name_lower.split():
                results.append({"id": item["id"], "name": item["name"]})
            elif search_type == 'contains' and search_term_lower in item_name_lower:
                results.append({"id": item["id"], "name": item["name"]})
            elif search_type == 'regex':
                pattern = re.compile(rf'\b{re.escape(search_term_lower)}\b')
                if pattern.search(item_name_lower):
                    results.append({"id": item["id"], "name": item["name"]})

        return jsonify(results)

    except json.JSONDecodeError:
        return jsonify({"error": "Formato inválido no arquivo de dados"}), 500
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500
