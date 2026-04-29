import requests
import time
from datetime import datetime
import random

# URL do endpoint no servidor Flask
URL_SERVIDOR = "http://127.0.0.1:5000/alertas"

BUEIROS = [
    {
        'id_bueiro': 'BUEIRO_01',
        'localizacao': 'Iguatemi',
        'nivel_atual': 0
    },
    {
        'id_bueiro': 'BUEIRO_02',
        'localizacao': 'Arenoso',
        'nivel_atual': 0
    },
    {
        'id_bueiro': 'BUEIRO_03',
        'localizacao': 'Rio Vermelho',
        'nivel_atual': 0
    }
]

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
    while True:
        for bueiro in BUEIROS:
            nivel = bueiro['nivel_atual']
            chuva_ciclo = random.randint(0,15)
            nivel += chuva_ciclo
            status_chuva_atual = status_chuva(nivel)
            bueiro['nivel_atual'] = nivel

            dados_sensor = {
                "id_bueiro": bueiro['id_bueiro'],
                "nivel_agua_cm": nivel,
                "status": status_chuva_atual,
                "timestamp": datetime.now().isoformat(),
                "localizacao": bueiro['localizacao']
            }

            if status_chuva_atual != "ALERTA_VERDE":
                enviar_alerta(dados_sensor)
            else:
                print(f"[SENSOR] do bueiro {dados_sensor['id_bueiro']}, no bairro {dados_sensor['localizacao']}. Nível normal: {nivel}cm - ALERTA_VERDE. Aguardando...")
        print("")
        time.sleep(7)
    


