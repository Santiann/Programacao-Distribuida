# FCoin - Sistema Distribuído de Validação de Transações

Sistema distribuído que simula o processo de validação de uma moeda digital usando o algoritmo **Proof of Stake (PoS)**, dividido nas camadas **Banco**, **Seletor** e **Validador**. A arquitetura permite consenso descentralizado, validações concorrentes e identificação de validadores maliciosos.

---

## 📚 Sumário

- [🔧 Tecnologias](#-tecnologias)
- [🏗️ Arquitetura](#-arquitetura)
- [🧠 Regras do Sistema](#-regras-do-sistema)
  - [Validação](#validação)
  - [Seleção de Validadores](#seleção-de-validadores)
  - [Recompensas e Penalidades](#recompensas-e-penalidades)
- [🚀 Como Executar](#-como-executar)
- [📄 Licença](#-licença)

---

## 🔧 Tecnologias

- Python 3.12
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- HTTP (RESTful API)

---

## 🏗️ Arquitetura

| Camada    | Função |
|-----------|--------|
| 🏦 **Banco (porta 5000)** | Gerencia clientes, registra transações, inicia o processo de validação |
| 🧠 **Seletor (porta 5001)** | Seleciona validadores com base no PoS, envia transações e calcula consenso |
| 🛡️ **Validadores (portas 5002 a 5011)** | Validam transações de forma autônoma e retornam status (conforme regras) |

---

## 🧠 Regras do Sistema

### 🔍 Validação

Um validador deve:
- Verificar se o **remetente tem saldo suficiente**
- Garantir que o **horário da transação seja válido** (não no futuro e maior que a última)
- Rejeitar se o **remetente fez mais de 1000 transações no último segundo**
- Validar somente se sua **chave única** bater com o registro no seletor

**Status possíveis:**
- `0`: Não executada
- `1`: Aprovada
- `2`: Rejeitada

---

### 🧮 Seleção de Validadores

- São escolhidos entre **3 a 5 validadores**
- A chance de seleção é baseada nos **FCoins apostados**
- Percentual mínimo: 5% / máximo: 40%
- Se menos de 3 validadores estiverem ativos, a transação fica em espera (até 1 min)

---

### 💰 Recompensas e Penalidades

- Validadores que acertam ganham uma fração da transação (via seletor)
- Se erram, recebem **uma flag**
- Com **3 flags**, são eliminados
- A cada 10.000 transações corretas, uma flag é removida
- O seletor também recebe parte da recompensa

---

## 🚀 Como Executar

### 1. Instalar dependências

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Rodar os serviços do sistema

> Recomendado: abrir um terminal separado para cada processo

#### 🏦 Banco (porta 5000)
```bash
python3 main.py
```

#### 🧠 Seletor (porta 5001)
```bash
python3 run_seletor.py
```

#### 🛡️ Para cadastrar os validadores (portas 5002 a 5011)
```bash
python3 app/validators/cadastro_validador.py
```

#### 🛡️ Para subir os validadores (portas 5002 a 5011)
```bash
python3 app/validators/subir_validadores.py 
```

#### 🛡️ Para matar todos os validadores (portas 5002 a 5011)
```bash
pkill -f run_validador.py
```

Esse script irá:
- Iniciar todos os validadores (inclusive o malicioso)
- Cadastrá-los automaticamente no seletor com seus respectivos FCoins

---

## 📄 Licença

MIT © 2025 — Desenvolvido para fins acadêmicos no contexto da disciplina **Programação Distribuída**