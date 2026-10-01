# 🚨 Sistema Inteligente de Alerta Preventivo de Alagamentos

Projeto de Atividade Extensionista — Bacharelado em Engenharia de Software
Centro Universitário Internacional UNINTER

---

## 📌 Sobre o Projeto

Sistema de simulação que reproduz o comportamento de sensores de nível de água em bueiros urbanos. Desenvolvido com foco em comunidades vulneráveis de Salvador/BA — regiões com histórico recorrente de alagamentos durante períodos de chuvas intensas.

Múltiplos bueiros são monitorados de forma independente, cada um com sua própria intensidade de chuva e nível de água. Quando o nível atinge limites críticos, o sistema classifica o alerta correspondente. Um dashboard web exibe o estado de todos os bueiros em tempo real, com atualização automática a cada 7 segundos.

O projeto foi desenvolvido como **prova de conceito (PoC)**, simulando o comportamento de uma solução de IoT sem depender de hardware físico.

---

## 🎯 Objetivos de Desenvolvimento Sustentável (ODS)

- **ODS 09** — Indústria, inovação e infraestrutura
- **ODS 11** — Cidades e comunidades sustentáveis
- **ODS 13** — Ação contra a mudança global do clima

---

## 🏗️ Arquitetura
 
```
                ┌────────────────────────────────┐
                │            app.py               │
                │           (Flask)               │
                │                                  │
                │  ┌────────────────────────────┐  │
                │  │   Thread do simulador       │  │
                │  │   (roda em segundo plano)   │  │
                │  │                              │  │
                │  │  • Cadeia de Markov          │  │
                │  │  • Distribuição Gama         │  │
                │  │  • Gera novo alerta a cada   │  │
                │  │    7 segundos                │  │
                │  └─────────────┬────────────────┘  │
                │                │ atualiza           │
                │                ▼                    │
                │        lista_alertas (memória)      │
                │                │                     │
                │      ┌─────────┴─────────┐           │
                │      ▼                   ▼           │
                │  GET /alertas      GET /  (index.html)│
                └────────────────────────────────┘
                               │
                               ▼
                     Navegador (dashboard)
```

---

## 🚦 Níveis de Alerta

| Status | Nível de Água | Significado |
|---|---|---|
| 🟢 ALERTA_VERDE | 0 — 29 cm | Nível seguro |
| 🟡 ALERTA_AMARELO | 30 — 59 cm | Começando a encher |
| 🟠 ALERTA_LARANJA | 60 — 89 cm | Próximo do limite |
| 🔴 ALERTA_VERMELHO | 90+ cm | Nível crítico |

---

## 🌧️ Modelagem da Chuva

A intensidade da chuva não é gerada de forma puramente aleatória. Ela segue um modelo probabilístico em duas etapas, pensado para se aproximar do comportamento real de eventos climáticos — que tendem a se intensificar ou enfraquecer de forma gradual, e não a saltar aleatoriamente entre extremos.

### 1. Cadeia de Markov (estado da chuva)

O estado de chuva de cada bueiro no ciclo atual depende do estado do ciclo anterior, conforme a matriz de transição de probabilidades:

| Estado atual | Sem chuva | Fraca | Moderada | Forte | Muito forte |
|---|---|---|---|---|---|
| **Sem chuva** | 75% | 25% | — | — | — |
| **Fraca** | 35% | 40% | 25% | — | — |
| **Moderada** | — | 35% | 40% | 25% | — |
| **Forte** | — | — | 50% | 30% | 20% |
| **Muito forte** | — | — | — | 80% | 20% |

### 2. Distribuição Gama (intensidade em cm)

Uma vez sorteado o novo estado, a quantidade de água acumulada naquele ciclo (em cm) é gerada por uma **distribuição Gama**, adequada para modelar variáveis contínuas e não negativas como volume de chuva:

| Estado | Shape | Scale |
|---|---|---|
| Fraca | 2 | 1.5 |
| Moderada | 2 | 2.5 |
| Forte | 2 | 4 |
| Muito forte | 2 | 5 |

No estado "sem chuva", simula-se o escoamento natural da água (drenagem), reduzindo levemente o nível acumulado. O nível nunca cai abaixo de zero.

Cada bueiro possui seu próprio estado de chuva, evoluindo de forma independente — simulando variações climáticas regionais dentro da mesma cidade.

---

## 🛠️ Tecnologias

- **Python 3.10+**
- **Flask** — servidor, API REST e execução da simulação
- **numpy** — geração da distribuição Gama
- **random** — sorteio dos estados da Cadeia de Markov
- **threading** — execução do simulador em segundo plano, junto do servidor
- **datetime** — timestamp dos alertas
- **HTML, CSS e JavaScript** — dashboard de monitoramento com auto-refresh

---

## 📁 Estrutura do Projeto
 
```
simulador-alerta-bueiro/
│
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── app.py              # API Flask + simulação (thread interna) + rota do dashboard
└── templates/
    └── index.html      # Dashboard de monitoramento em tempo real
```

## ✅ Pré-requisitos

- [Python 3.10 ou superior](https://www.python.org/downloads/) instalado
- `pip` atualizado (`pip install --upgrade pip`)

---

## ▶️ Como Executar

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd simulador-alerta-bueiro
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

Conteúdo do `requirements.txt`:

```
Flask==3.0.0
requests==2.31.0
numpy==1.26.4
```

### 3. Iniciar o servidor

```bash
python app.py
```

### 4. Consultar o dashboard no navegador

```
http://127.0.0.1:5000/
```

---

## 🌐 Acesso Online

O projeto também está publicado e pode ser acessado diretamente pelo link abaixo, sem necessidade de instalação local:

```
https://simulador-alerta-bueiro.onrender.com
```

---

## 📡 Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Dashboard de monitoramento |
| GET | `/alertas` | Retorna todos os alertas registrados (JSON) |
| POST | `/alertas` | Permite registrar um alerta manualmente (mantido por compatibilidade/testes) |

**Exemplo de item retornado por `GET /alertas`:**

```json
{
  "id_bueiro": "BUEIRO_01",
  "nivel_agua_cm": 42.37,
  "status": "ALERTA_AMARELO",
  "timestamp": "2026-09-10T16:54:24.123456",
  "localizacao": "Iguatemi"
}
```

---

## 🧪 Testes Realizados

- Geração contínua de dados pela thread interna do simulador, sem bloquear as respostas da API;
- Classificação automática correta dos quatro níveis de alerta (verde, amarelo, laranja, vermelho);
- Atualização em tempo real do dashboard a cada ciclo de simulação (7 segundos);
- Comportamento coerente da geração de chuva (transições suaves entre estados, sem saltos abruptos);
- Execução estável do servidor com um único processo, sem duplicação da thread de simulação.

---

## 🗺️ Possíveis Melhorias Futuras

- Persistência dos alertas em banco de dados (atualmente em memória);
- Autenticação na API REST;
- Histórico gráfico de nível de água por bueiro ao longo do tempo;
- Integração com dados climáticos reais via API meteorológica;
- Notificações via e-mail/SMS em caso de alerta vermelho;
- Migração para um servidor WSGI de produção (ex: Gunicorn), em vez do servidor de desenvolvimento do Flask.

---

## 📄 Licença

Projeto acadêmico desenvolvido para fins educacionais, sem fins comerciais.

---

## 👩‍💻 Autora

**Yasmin Gonçalves de Souza**
Bacharelado em Engenharia de Software — UNINTER
Atividade Extensionista: Tecnologia Aplicada à Inclusão Digital
