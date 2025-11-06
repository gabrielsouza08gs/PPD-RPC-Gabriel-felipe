PPD – Projeto RPC Miner (gRPC em Python)

Disciplina: Programação Paralela e Distribuída
Professor: Breno Krohling
Curso: Engenharia da Computação — Multivix

Alunos:
Gabriel Souza do Nascimento — 1-2215114
Felipe Colloddetti Ramos — 1-2212294



 1. Introdução

O presente relatório descreve o desenvolvimento de um sistema cliente-servidor baseado em RPC (Remote Procedure Call) utilizando o framework gRPC com a linguagem Python.
O objetivo principal foi compreender a comunicação entre processos distribuídos, o funcionamento de chamadas remotas e a aplicação prática de mineração de desafios (proof-of-work) simulando um ambiente distribuído.

 2. Metodologia e Arquitetura

O projeto foi implementado em Python 3.10+ utilizando as bibliotecas grpcio, grpcio-tools e protobuf.
A comunicação entre cliente e servidor foi definida através de um arquivo .proto (gRPC IDL) que contém os métodos remotos e as mensagens trocadas entre as partes.

Estrutura do sistema:
 rpc_miner/
 ┣  grpcCalc.proto
 ┣  server.py
 ┣  client.py
 ┣  build_stubs.py
 ┣  requirements.txt
 ┗  README.md

Principais métodos RPC definidos:

GetTransactionID – Retorna o ID atual da transação.

GetChallenge – Fornece o desafio (nível de dificuldade em zeros no hash SHA-1).

GetTransactionStatus – Retorna o estado da transação (pendente, resolvida ou inválida).

SubmitChallenge – Recebe a solução do cliente e valida o hash.

GetWinner – Retorna o ID do cliente vencedor.

GetSolution – Exibe a solução vencedora.


Funcionamento:

O servidor cria uma nova transação com um desafio aleatório entre MIN_CHALLENGE e MAX_CHALLENGE.

O cliente solicita o desafio, gera hashes (SHA-1) de forma concorrente e tenta encontrar uma string cujo hash inicie com N zeros.

Ao encontrar uma solução válida, o cliente envia via RPC e o servidor registra o vencedor, abrindo automaticamente a próxima transação.

🔬 3. Implementação

O servidor foi desenvolvido com ThreadPoolExecutor para permitir múltiplas conexões simultâneas.
O controle de concorrência e integridade das transações é feito por threading.Lock, evitando condições de corrida durante a validação das soluções.

No cliente, o processo de mineração foi paralelizado com múltiplas threads, cada uma testando diferentes nonces até encontrar uma solução.
A validação ocorre através da função SHA-1, e a dificuldade é proporcional à quantidade de zeros iniciais exigidos pelo desafio.

 4. Testes e Resultados

Foram realizados testes com diferentes níveis de dificuldade (1–10) e múltiplos clientes simultâneos.
Os resultados mostraram que o tempo de mineração cresce exponencialmente com o aumento do desafio, e o desempenho melhora linearmente com o número de threads no cliente.

Exemplo de execução:
[server] Listening on [::]:50051 (challenge 1..5)
[mine] transaction=2, challenge=3
[mine] local solution: client1:tid2:9176, sha1=000978f3c6c42f987864d0e3bf44f7124d8850a
[mine] server response result=1 (valid)

Observações:

Cada cliente que encontra a solução válida é registrado como vencedor.

Clientes que tentam submeter após a resolução recebem result=2 (already solved).

O servidor automaticamente gera a próxima transação após cada desafio concluído.

 5. Discussão

O experimento demonstrou de forma prática o conceito de RPC e sincronização entre processos distribuídos.
A estrutura do gRPC simplifica a definição da interface e a geração automática de código cliente/servidor, permitindo foco na lógica da aplicação.
Além disso, a mineração simulada permitiu observar aspectos como:

Latência de comunicação RPC;

Sincronização entre múltiplos clientes;

Impacto do paralelismo local (threads) no tempo de execução.

 6. Conclusões

O projeto cumpriu seu objetivo de implementar um sistema distribuído funcional usando RPC com gRPC, mostrando na prática a comunicação entre processos, concorrência e validação de resultados de forma síncrona e escalável.

A solução pode ser expandida futuramente com:

Interface web para visualização das transações;

Armazenamento dos resultados em banco de dados;

Ajuste dinâmico de dificuldade conforme taxa de soluções.

 7. Execução do Projeto
Requisitos:

Python 3.10 ou superior

Pacotes do requirements.txt

Passos:
pip install -r requirements.txt
python build_stubs.py
python server.py         # Inicia o servidor
python client.py --server localhost:50051 --client-id 1


Durante a execução, use a opção 6) Mine (auto) no cliente para resolver o desafio automaticamente.



