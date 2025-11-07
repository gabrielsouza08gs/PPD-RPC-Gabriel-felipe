Relatório Técnico — PPD / RPC (gRPC)

Professor: Breno Krohling
Alunos:

Gabriel Souza do Nascimento — 1-2215114

Felipe Collodetti Ramos — 1-2212294

1. Introdução

O trabalho teve como objetivo desenvolver dois sistemas baseados em comunicação RPC (Remote Procedure Call) utilizando o framework gRPC em Python:

Calculadora RPC, responsável por executar operações matemáticas básicas (soma, subtração, multiplicação e divisão) remotamente;

Minerador RPC, que simula um desafio de “mineração” distribuída, com múltiplos clientes tentando resolver um problema de hash para determinar um vencedor.

A proposta permitiu compreender conceitos de distribuição de tarefas, concorrência e comunicação entre processos usando o modelo cliente-servidor.

2. Metodologia de Implementação
2.1 Estrutura e Ferramentas

Ambos os sistemas foram implementados em Python 3.10, utilizando as bibliotecas:

grpcio

grpcio-tools

protobuf

Os arquivos .proto foram criados para definir os serviços, mensagens e métodos de comunicação entre cliente e servidor.
Os stubs (arquivos *_pb2.py e *_pb2_grpc.py) foram gerados com o comando:

python build_stubs.py

2.2 Arquitetura da Calculadora RPC

O servidor oferece quatro operações matemáticas.

O cliente possui um menu interativo que envia os valores e a operação desejada para o servidor.

O servidor processa a operação e retorna o resultado.

Há tratamento de divisão por zero.

2.3 Arquitetura do Minerador RPC

O servidor mantém variáveis de controle (TransactionID, Challenge, Solution, Winner).

O cliente possui opções para consultar o estado atual e executar automaticamente o processo de mineração (Mine (auto)).

A mineração consiste em encontrar um nonce que gere um hash SHA-1 com uma certa quantidade de zeros à esquerda, definida pela dificuldade do desafio.

Quando um cliente encontra a solução, o servidor registra o vencedor e passa para a próxima transação.

3. Testes e Resultados
3.1 Testes Realizados

Foram realizados testes individuais e simultâneos, conforme a seguir:

Calculadora:

Testes de todas as operações aritméticas.

Teste de erro de divisão por zero.

Teste com números negativos e decimais.

Minerador:

Execuções com diferentes níveis de dificuldade (Challenge = 1 até 5).

Testes com dois clientes simultâneos para verificar a competição e o tempo médio de mineração.

3.2 Resultados Obtidos

Calculadora: todas as operações responderam corretamente, retornando resultados exatos. O tratamento de divisão por zero funcionou adequadamente.

Minerador: observou-se que:

Com desafios simples (Challenge baixo), o resultado é encontrado rapidamente.

Com maior dificuldade, o tempo de execução aumenta de forma exponencial.

Ao executar com mais de um cliente, há disputa, e o primeiro que encontra a solução é registrado como vencedor.

3.3 Análise

O desempenho do sistema RPC foi satisfatório. A comunicação entre cliente e servidor mostrou-se estável, com tempo de resposta rápido.
Os resultados evidenciam a escalabilidade e a capacidade do gRPC de lidar com múltiplas conexões simultâneas.

4. Conclusão

O projeto permitiu aplicar, na prática, os conceitos de RPC e programação distribuída.
Com a Calculadora RPC, foi possível compreender o fluxo básico de chamadas remotas;
com o Minerador RPC, foi explorada a ideia de competição e paralelismo entre clientes.

A implementação mostrou que o uso de gRPC em Python é uma ferramenta eficiente, modular e com boa capacidade de expansão para projetos mais complexos.

 Instruções para Compilação e Execução

Os projetos Calculadora RPC e Minerador RPC foram desenvolvidos em Python 3.10+, utilizando o framework gRPC para comunicação entre cliente e servidor.

Criar ambiente virtual:

python -m venv .venv
.\.venv\Scripts\activate


Instalar dependências:

pip install -r requirements.txt


Gerar stubs gRPC (apenas na primeira execução):

python build_stubs.py


Executar o servidor:

Calculadora → Porta 50052

Minerador → Porta 50053

python server.py


Executar o cliente:

python client.py --server localhost:PORTA
