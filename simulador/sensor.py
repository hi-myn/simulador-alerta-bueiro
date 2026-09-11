import requests
import time
from datetime import datetime
import random
import numpy as np

# URL do endpoint no servidor Flask
URL_SERVIDOR = "http://127.0.0.1:5000/alertas"

BUEIROS = [
    {"id_bueiro": "BUEIRO_01", "localizacao": "Iguatemi", "nivel_atual": 0, "intensidade_chuva": "sem_chuva"},
    {"id_bueiro": "BUEIRO_02", "localizacao": "Arenoso", "nivel_atual": 0, "intensidade_chuva": "sem_chuva"},
    {"id_bueiro": "BUEIRO_03", "localizacao": "Rio Vermelho", "nivel_atual": 0, "intensidade_chuva": "sem_chuva"},
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


def enviar_alerta(dados_sensor):
    """
    Envia um dicionário com os dados do sensor para o servidor via requisição POST.
    """
    try:
        print(f"[SIMULADOR] Enviando dados para {URL_SERVIDOR}...")

        # Serializa o dicionário para JSON e envia na requisição POST com o header apropriado
        resposta = requests.post(
            URL_SERVIDOR,
            json=dados_sensor,
            headers={"Content-Type": "application/json"},
        )

        # Verifica se o servidor respondeu com sucesso
        if resposta.status_code == 200:
            print("[SIMULADOR] Dados enviados com sucesso e recebidos pelo servidor!")
            print(f" > Resposta do servidor: {resposta.json()}")
        else:
            print(
                f"[SIMULADOR] Falha no envio. Código de status HTTP: {resposta.status_code}"
            )

    except requests.exceptions.ConnectionError:
        print("[SIMULADOR] ERRO: Não foi possível conectar ao servidor.")
        print(" > Certifique-se de que o servidor (app.py) está em execução.")
    except Exception as e:
        print(f"[SIMULADOR] Ocorreu um erro inesperado: {e}")


def status_chuva(nivel):
    if nivel < 30:
        return "ALERTA_VERDE"
    elif nivel < 60:
        return "ALERTA_AMARELO"
    elif nivel < 90:
        return "ALERTA_LARANJA"
    else:
        return "ALERTA_VERMELHO"


if __name__ == "__main__":
    while True:
        for bueiro in BUEIROS:
            nivel = bueiro["nivel_atual"]

            estado_atual = bueiro["intensidade_chuva"]
            opcoes = list(MATRIZ_TRANSICAO[estado_atual].keys())
            pesos = list(MATRIZ_TRANSICAO[estado_atual].values())

            novo_estado = random.choices(opcoes, weights=pesos, k=1)[0]

            if novo_estado == "sem_chuva":
                intensidade_cm = -random.randint(0,2)
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
                "nivel_agua_cm": nivel,
                "status": status_chuva_atual,
                "timestamp": datetime.now().isoformat(),
                "localizacao": bueiro["localizacao"],
            }

            enviar_alerta(dados_sensor)

        print("")
        time.sleep(7)
