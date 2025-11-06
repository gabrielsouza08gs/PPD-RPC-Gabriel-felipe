
# PPD – RPC Miner (Python/gRPC)

Protótipo cliente/servidor baseado em RPC com gRPC, incluindo menu interativo e mineração multi‑thread local.

## Requisitos
- Python 3.10+
- `pip install -r requirements.txt`

## Geração dos Stubs
```bash
python build_stubs.py
# isto gera grpcCalc_pb2.py e grpcCalc_pb2_grpc.py
```

## Execução
Servidor (terminal 1):
```bash
# opcionais: export MINER_PORT=50051 MIN_CHALLENGE=1 MAX_CHALLENGE=5
python server.py
```

Cliente (terminal 2):
```bash
python client.py --server localhost:50051 --client-id 42
```

No menu do cliente, use **Mine** para procurar uma solução local (sha1(solution) iniciando com `challenge` zeros) e submetê-la.

### Observações
- Por padrão, o servidor cria desafios com dificuldade `1..5` para execuções rápidas. Para a atividade, você pode aumentar até `20` via `MAX_CHALLENGE`.
- Quando uma transação é solucionada, o servidor abre automaticamente a próxima (TransactionID + 1).

## Estrutura da Tabela Mantida pelo Servidor
- `TransactionID` (int): ID da transação corrente
- `Challenge` (int): nível de dificuldade (nº de zeros à esquerda no SHA‑1)
- `Solution` (string): solução vencedora
- `Winner` (int): ClientID vencedor

## Relatório Técnico (modelo sugerido)
1. **Introdução**: objetivo do uso de RPC e do gRPC no contexto.
2. **Metodologia**: como a interface `.proto` foi definida; mapeamento dos métodos RPC; política de geração de desafios.
3. **Arquitetura**: diagrama simples cliente ↔ servidor, threads do cliente, estados no servidor.
4. **Implementação**: decisões (formato da solução, verificação SHA‑1, controle de concorrência, abertura de nova transação).
5. **Testes**: casos (diferentes dificuldades, múltiplos clientes), métricas (tempo médio para achar solução, nº de threads).
6. **Resultados e Discussão**: análise do impacto de `challenge`, escalabilidade e limitações.
7. **Conclusões e Trabalhos Futuros**.
8. **Como Executar**: passos de build e execução (resumo).
9. **Vídeo**: link para mini‑demonstração (≤ 5 min).

> Prazo no enunciado: 08/11/2025.
