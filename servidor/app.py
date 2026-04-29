from flask import Flask, request, jsonify, render_template # type: ignore

app = Flask(__name__)

lista_alertas = []


@app.route('/alertas', methods=['POST'])
def receber_alerta():
    """
    Endpoint para receber os dados simulados do sensor do bueiro.
    Espera receber um payload no formato JSON.
    """
    try:
        # Extrai os dados em formato JSON da requisição
        dados_recebidos = request.get_json()
        
        # Aqui, na versão boilerplate, apenas imprimimos o JSON no console
        print(f"[SERVIDOR] Alerta Recebido:")
        print(f" > Dados: {dados_recebidos}")
        print("")

        lista_alertas.append(dados_recebidos)
        
        # Responde ao cliente que enviou os dados
        return jsonify({
            "status": "sucesso",
            "mensagem": "Alerta recebido com sucesso!"
        }), 200
    
        
        
    except Exception as e:
        # Tratamento de erro básico
        print(f"[SERVIDOR] Erro ao processar o alerta: {e}")
        return jsonify({
            "status": "erro",
            "mensagem": "Falha ao processar a requisição."
        }), 400

@app.route('/alertas', methods=['GET'])
def retorna_alerta():
    try:
        return jsonify(lista_alertas),200
    except Exception as e:
        # Tratamento de erro básico
        print(f"[SERVIDOR] Erro ao retornar o alerta: {e}")
        return jsonify({
            "status": "erro",
            "mensagem": "Falha ao processar a requisição."
        }), 400

@app.route('/', methods=['GET'])
def page():
    return render_template('index.html')

if __name__ == '__main__':
    # Inicia o servidor Flask na porta 5000
    print("[SERVIDOR] Iniciando o servidor de alertas na porta 5000...")
    app.run(debug=True, host='0.0.0.0', port=5000)
