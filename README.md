# 🚨 Sistema Inteligente de Alerta Preventivo de Alagamentos

Projeto de Atividade Extensionista III — Bacharelado em Engenharia de Software  
Centro Universitário Internacional UNINTER

---

## 📌 Sobre o Projeto

Sistema de simulação que reproduz o comportamento de sensores de nível de água em bueiros urbanos. Desenvolvido com foco em comunidades vulneráveis de Salvador/BA — regiões com histórico recorrente de alagamentos durante períodos de chuvas intensas.

Quando o nível da água simulado atinge limites críticos, o sensor envia alertas automáticos para um servidor central via API REST, permitindo monitoramento em tempo real.

---

## 🎯 Objetivos de Desenvolvimento Sustentável (ODS)

- **ODS 09** — Indústria, inovação e infraestrutura
- **ODS 11** — Cidades e comunidades sustentáveis
- **ODS 13** — Ação contra a mudança global do clima

---

## 🏗️ Arquitetura

```
[sensor.py]  →  HTTP POST (JSON)  →  [app.py]
  Simulador                           Servidor Flask
  Gera dados                          Recebe alertas
  Decide status                       Armazena histórico
  Roda independente                   Expõe API REST
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

## 🛠️ Tecnologias

- **Python 3.x**
- **Flask** — servidor e API REST
- **requests** — comunicação HTTP no simulador
- **random** — simulação de intensidade de chuva
- **datetime** — timestamp dos alertas

---

## 📁 Estrutura do Projeto

```
simulador-alerta-bueiro/
│
├── servidor/
│   └── app.py          # API Flask — recebe e armazena alertas
│
└── simulador/
    └── sensor.py       # Simula sensores nos bueiros
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
| POST | `/alertas` | Recebe um alerta do sensor |
| GET | `/alertas` | Retorna todos os alertas registrados |

---

## 👩‍💻 Autora

**Yasmin Gonçalves de Souza** 
Bacharelado em Engenharia de Software — UNINTER