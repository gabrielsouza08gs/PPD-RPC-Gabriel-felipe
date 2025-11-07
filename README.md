
# Atividade 1 — Calculadora RPC (Python + gRPC)

Implementação de um serviço RPC de calculadora com **menu interativo** no cliente:
Soma, Subtração, Multiplicação e Divisão (com tratamento de divisão por zero).

## Passo a passo (VS Code)
1. Abrir a pasta no VS Code.
2. (Opcional) Criar/ativar venv:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Instalar dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Gerar stubs:
   ```bash
   python build_stubs.py
   ```
5. Rodar o servidor (Terminal 1):
   ```bash
   python server.py
   ```
6. Rodar o cliente (Terminal 2):
   ```bash
   python client.py --server localhost:50051
   ```
7. Seguir o **menu** e testar as quatro operações.

## Notas
- A enum `Op` no `.proto` padroniza as operações.
- O servidor retorna `err`/`err_msg` quando há **divisão por zero**.
