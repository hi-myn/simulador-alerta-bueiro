# 🚨 Sistema Inteligente de Alerta Preventivo de Alagamentos

Projeto de Atividade Extensionista III — Bacharelado em Engenharia de Software  
Centro Universitário Internacional UNINTER

---

## 📌 Sobre o Projeto

Sistema de simulação que reproduz o comportamento de sensores de nível de água em bueiros urbanos. Desenvolvido com foco em comunidades vulneráveis de Salvador/BA — regiões com histórico recorrente de alagamentos durante períodos de chuvas intensas.
 
Múltiplos sensores simulados monitoram bueiros de forma independente, cada um com sua própria intensidade de chuva e nível de água. Quando o nível atinge limites críticos, o sensor envia alertas automáticos para um servidor central via API REST. Um dashboard web exibe o estado de todos os bueiros em tempo real, com atualização automática a cada 7 segundos.

---

## 🎯 Objetivos de Desenvolvimento Sustentável (ODS)

- **ODS 09** — Indústria, inovação e infraestrutura
- **ODS 11** — Cidades e comunidades sustentáveis
- **ODS 13** — Ação contra a mudança global do clima

---

## 🏗️ Arquitetura

```
[sensor.py]  →  HTTP POST (JSON)  →  [app.py]  →  [index.html]
  Simulador                           Servidor        Dashboard
  3 bueiros                           Flask           Tempo real
  Chuva aleatória                     API REST        Auto-refresh
  Escoamento                          Histórico       Visualização
```

Os dois módulos rodam como **processos independentes**, comunicando-se pela rede local via protocolo HTTP — simulando uma arquitetura distribuída real.

---

## 🚦 Níveis de Alerta

| Status | Nível de Água | Significado |
|---|---|---|
| 🟢 ALERTA_VERDE | 0 — 29 cm | Nível seguro |
| 🟡 ALERTA_AMARELO | 30 — 59 cm | Começando a encher |
| 🟠 ALERTA_LARANJA | 60 — 89 cm | Próximo do limite |
| 🔴 ALERTA_VERMELHO | 90+ cm | Nível crítico |

---

## 🌧️ Simulação de Chuva
 
A intensidade da chuva é gerada probabilisticamente por ciclo, baseada em dados climáticos reais de Salvador/BA:
 
| Cenário | Probabilidade | Variação do nível |
|---|---|---|
| Sem chuva / drenagem | 30% | -1 a -5 cm |
| Chuva fraca | 40% | +1 a +5 cm |
| Chuva moderada | 20% | +1 a +10 cm |
| Chuva forte | 8% | +1 a +15 cm |
| Chuva muito forte | 2% | +1 a +20 cm |
 
Cada bueiro recebe sua própria intensidade de chuva por ciclo, simulando variações climáticas por região. O nível nunca cai abaixo de zero.
 
---

## 🛠️ Tecnologias

- **Python 3.x**
- **Flask** — servidor e API REST
- **requests** — comunicação HTTP no simulador
- **random** — simulação de intensidade de chuva
- **datetime** — timestamp dos alertas
- **HTML, CSS e JavaScript** — dashboard de monitoramento com auto-refresh

---

## 📁 Estrutura do Projeto

```
simulador-alerta-bueiro/
│
├── README.md
├── requirements.txt
│
├── servidor/
│   ├── app.py              # API Flask — recebe e armazena alertas
│   └── templates/
│       └── index.html      # Dashboard de monitoramento em tempo real
│
└── simulador/
    └── sensor.py           # Simula sensores nos bueiros
```

---

## ▶️ Como Executar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Iniciar o servidor (Terminal 1)

```bash
cd servidor
python app.py
```

### 3. Iniciar o simulador (Terminal 2)

```bash
cd simulador
python sensor.py
```

### 4. Consultar alertas no navegador

```
http://127.0.0.1:5000/
```

---

## 📡 Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Dashboard de monitoramento |
| POST | `/alertas` | Recebe um alerta do sensor |
| GET | `/alertas` | Retorna todos os alertas registrados (JSON) |

---

## 👩‍💻 Autora

**Yasmin Gonçalves de Souza** 
Bacharelado em Engenharia de Software — UNINTER