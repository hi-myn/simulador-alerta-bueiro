import os
import time
import random
import threading
from datetime import datetime

import numpy as np
from flask import Flask, request, jsonify, render_template  # type: ignore

app = Flask(__name__)

lista_alertas = []

# Configuração da simulação (antes vivia em sensor.py, agora roda em thread
# dentro do próprio servidor, sem precisar de um segundo processo/terminal)

BUEIROS = [
    {
        "id_bueiro": "BUEIRO_01",
        "localizacao": "Iguatemi",
        "nivel_atual": 0,
        "intensidade_chuva": "sem_chuva",
    },
    {
        "id_bueiro": "BUEIRO_02",
        "localizacao": "Arenoso",
        "nivel_atual": 0,
        "intensidade_chuva": "sem_chuva",
    },
    {
        "id_bueiro": "BUEIRO_03",
        "localizacao": "Rio Vermelho",
        "nivel_atual": 0,
        "intensidade_chuva": "sem_chuva",
    },
]

MATRIZ_TRANSICAO = {
    "sem_chuva": {
        "sem_chuva": 0.75,
        "fraca": 0.25,
    },
    "fraca": {
        "sem_chuva": 0.35,
        "fraca": 0.40,
        "moderada": 0.25,
    },
    "moderada": {
        "fraca": 0.35,
        "moderada": 0.40,
        "forte": 0.25,
    },
    "forte": {
        "moderada": 0.50,
        "forte": 0.30,
        "muito_forte": 0.20,
    },
    "muito_forte": {
        "forte": 0.80,
        "muito_forte": 0.20,
    },
}

PARAMETROS_GAMA = {
    "fraca": {"shape": 2, "scale": 1.5},
    "moderada": {"shape": 2, "scale": 2.5},
    "forte": {"shape": 2, "scale": 4},
    "muito_forte": {"shape": 2, "scale": 5},
}


def status_chuva(nivel):
    if nivel < 30:
        return "ALERTA_VERDE"
    elif nivel < 60:
        return "ALERTA_AMARELO"
    elif nivel < 90:
        return "ALERTA_LARANJA"
    else:
        return "ALERTA_VERMELHO"


def ciclo_simulacao():
    """
    Executa um ciclo de simulação para todos os bueiros e adiciona os
    alertas gerados diretamente na lista_alertas (em memória).
    """
    for bueiro in BUEIROS:
        nivel = bueiro["nivel_atual"]

        estado_atual = bueiro["intensidade_chuva"]
        opcoes = list(MATRIZ_TRANSICAO[estado_atual].keys())
        pesos = list(MATRIZ_TRANSICAO[estado_atual].values())

        novo_estado = random.choices(opcoes, weights=pesos, k=1)[0]

        if novo_estado == "sem_chuva":
            intensidade_cm = -random.randint(0, 2)
        else:
            params = PARAMETROS_GAMA[novo_estado]
            intensidade_cm = np.random.gamma(params["shape"], params["scale"])

        nivel += intensidade_cm
        nivel = max(0, nivel)

        status_chuva_atual = status_chuva(nivel)
        bueiro["nivel_atual"] = nivel
        bueiro["intensidade_chuva"] = novo_estado

        dados_sensor = {
            "id_bueiro": bueiro["id_bueiro"],
            "nivel_agua_cm": round(nivel, 2),
            "status": status_chuva_atual,
            "timestamp": datetime.now().isoformat(),
            "localizacao": bueiro["localizacao"],
        }

        print(f"[SIMULADOR] Novo alerta gerado: {dados_sensor}")
        lista_alertas.append(dados_sensor)


def loop_simulador(intervalo_segundos=7):
    """
    Loop infinito que roda em uma thread separada, gerando novos dados
    de simulação a cada N segundos, sem bloquear o servidor Flask.
    """
    while True:
        ciclo_simulacao()
        time.sleep(intervalo_segundos)


# Rotas da API


@app.route("/alertas", methods=["POST"])
def receber_alerta():
    """
    Mantido por compatibilidade: ainda é possível enviar um alerta
    manualmente via POST, caso necessário para testes.
    """
    try:
        dados_recebidos = request.get_json()

        print(f"[SERVIDOR] Alerta Recebido:")
        print(f" > Dados: {dados_recebidos}")
        print("")

        lista_alertas.append(dados_recebidos)

        return (
            jsonify({"status": "sucesso", "mensagem": "Alerta recebido com sucesso!"}),
            200,
        )

    except Exception as e:
        print(f"[SERVIDOR] Erro ao processar o alerta: {e}")
        return (
            jsonify({"status": "erro", "mensagem": "Falha ao processar a requisição."}),
            400,
        )


@app.route("/alertas", methods=["GET"])
def retorna_alerta():
    try:
        return jsonify(lista_alertas), 200
    except Exception as e:
        print(f"[SERVIDOR] Erro ao retornar o alerta: {e}")
        return (
            jsonify({"status": "erro", "mensagem": "Falha ao processar a requisição."}),
            400,
        )


@app.route("/", methods=["GET"])
def page():
    return render_template("index.html")


# Inicialização: inicia a thread do simulador junto com o servidor


def iniciar_simulador_em_thread():
    thread = threading.Thread(target=loop_simulador, daemon=True)
    thread.start()


if __name__ == "__main__":
    print("[SERVIDOR] Iniciando simulador em thread de segundo plano...")
    iniciar_simulador_em_thread()

    print("[SERVIDOR] Iniciando o servidor de alertas na porta 5000...")

    porta = int(os.environ.get("PORT", 5000))
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=porta)
