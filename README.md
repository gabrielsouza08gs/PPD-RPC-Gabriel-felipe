
Relatório Técnico — PPD / RPC (gRPC)

Professor: Breno Krohling
Alunos:
Gabriel Souza do Nascimento — 1-2215114

Felipe Collodetti Ramos — 1-2212294

Instruções para Compilação e Execução

 Requisitos do Ambiente

Sistema Operacional: Windows 10 ou superior

Python: versão 3.10 ou superior

Bibliotecas necessárias:

grpcio

grpcio-tools

protobuf

Essas bibliotecas podem ser instaladas automaticamente pelo arquivo requirements.txt.

 Criação do Ambiente Virtual

Antes de executar os projetos, é recomendado criar um ambiente virtual para isolar as dependências:

python -m venv .venv


Ativar o ambiente (no Windows PowerShell):

.\.venv\Scripts\activate


Se o PowerShell bloquear a ativação, pode-se usar o comando alternativo:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\.venv\Scripts\Activate.ps1

 Instalação das Dependências

Com o ambiente virtual ativo, instale as dependências do projeto:

pip install -r requirements.txt

 Execução da Calculadora RPC

Gerar os stubs gRPC (apenas na primeira vez):

python build_stubs.py


Executar o servidor da calculadora (porta padrão 50052):

$env:CALC_PORT=50052
python server.py


O terminal exibirá algo como:

[server] Calculadora RPC escutando em 0.0.0.0:50052


Executar o cliente da calculadora (em outro terminal):

python client.py --server localhost:50052


Será exibido um menu interativo com as operações:

===== CALCULADORA RPC =====
1) Soma (a + b)
2) Subtração (a - b)
3) Multiplicação (a * b)
4) Divisão (a / b)
0) Sair


O usuário escolhe a operação e informa os valores.
O resultado é processado no servidor e retornado ao cliente.

 Execução do RPC Miner (Mineração)

Gerar os stubs gRPC (apenas na primeira vez):

python build_stubs.py


Executar o servidor da mineração (porta padrão 50053):

$env:MINER_PORT=50053
python server.py


O terminal mostrará:

[server] RPC Miner escutando em 0.0.0.0:50053


Executar o cliente (em outro terminal):

python client.py --server localhost:50053 --client-id 1


O menu do minerador será exibido:

==== RPC Miner Client ====
1) getTransactionID
2) getChallenge
3) getTransactionStatus
4) getWinner
5) getSolution
6) Mine (auto)
0) Exit
