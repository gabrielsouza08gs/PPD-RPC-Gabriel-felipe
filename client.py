
import argparse

import grpc

import grpc_calc_pb2 as pb2
import grpc_calc_pb2_grpc as pb2_grpc

MENU = """
===== CALCULADORA RPC =====
1) Soma (a + b)
2) Subtração (a - b)
3) Multiplicação (a * b)
4) Divisão (a / b)
0) Sair
"""

def read_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip().replace(',', '.'))
        except ValueError:
            print("Valor inválido. Tente novamente.")

def choose_op() -> int:
    print(MENU)
    while True:
        try:
            c = int(input("Escolha: ").strip())
        except ValueError:
            c = -9
        if c in (0,1,2,3,4):
            return c
        print("Opção inválida.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--server", default="localhost:50051")
    args = ap.parse_args()

    channel = grpc.insecure_channel(args.server)
    stub = pb2_grpc.CalcServiceStub(channel)
    print(f"Conectado ao servidor {args.server}.")

    while True:
        choice = choose_op()
        if choice == 0:
            print("Saindo...")
            break

        a = read_float("Informe a: ")
        b = read_float("Informe b: ")

        op_map = {1: pb2.ADD, 2: pb2.SUB, 3: pb2.MUL, 4: pb2.DIV}
        req = pb2.ComputeRequest(op=op_map[choice], a=a, b=b)
        resp = stub.Compute(req)

        if resp.err != 0:
            print(f"[ERRO] {resp.err_msg} (código {resp.err})\n")
        else:
            print(f"Resultado: {resp.result}\n")

if __name__ == "__main__":
    main()
