import requests
import time
from datetime import datetime
import random

# URL do endpoint no servidor Flask
URL_SERVIDOR = "http://127.0.0.1:5000/alertas"

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
            headers={'Content-Type': 'application/json'}
        )
        
        # Verifica se o servidor respondeu com sucesso
        if resposta.status_code == 200:
            print("[SIMULADOR] Dados enviados com sucesso e recebidos pelo servidor!")
            print(f" > Resposta do servidor: {resposta.json()}")
        else:
            print(f"[SIMULADOR] Falha no envio. Código de status HTTP: {resposta.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("[SIMULADOR] ERRO: Não foi possível conectar ao servidor.")
        print(" > Certifique-se de que o servidor (app.py) está em execução.")
    except Exception as e:
        print(f"[SIMULADOR] Ocorreu um erro inesperado: {e}")

def status_chuva(nivel):
    if nivel < 30 :
        return "ALERTA_VERDE"
    elif nivel < 60:
        return "ALERTA_AMARELO"
    elif nivel < 90:
        return "ALERTA_LARANJA"
    else:
        return "ALERTA_VERMELHO"

if __name__ == "__main__":
    nivel_atual = 0
    while True:
        chuva_ciclo = random.randint(0,15)
        nivel_atual += chuva_ciclo
        status_chuva_atual = status_chuva(nivel_atual)
        dados_sensor = {
            "id_bueiro": "BUEIRO_CENTRO_01",
            "nivel_agua_cm": nivel_atual,
            "status": status_chuva_atual,
            "timestamp": datetime.now().isoformat()
        }
        if status_chuva_atual != "ALERTA_VERDE":
            enviar_alerta(dados_sensor)
        else:
            print(f"[SENSOR] Nível normal: {nivel_atual}cm - ALERTA_VERDE. Aguardando...")
        time.sleep(5)
    


