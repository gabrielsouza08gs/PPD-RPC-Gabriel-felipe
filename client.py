
import argparse
import hashlib
import threading
import time
from concurrent import futures

import grpc

import grpcCalc_pb2 as pb2
import grpcCalc_pb2_grpc as pb2_grpc

def sha1_hex(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()

def mine_local(prefix: str, challenge: int, max_seconds: int = 60, workers: int = 8):
    """
    Brute-force a solution string such that sha1(solution) starts with '0'*challenge.
    We search solutions of the form f"{prefix}:{nonce}".
    """
    stop_flag = threading.Event()
    result = {"solution": None}

    def worker(start_nonce: int, step: int):
        nonce = start_nonce
        deadline = time.time() + max_seconds
        while not stop_flag.is_set() and time.time() < deadline:
            candidate = f"{prefix}:{nonce}"
            if sha1_hex(candidate).startswith("0" * max(0, challenge)):
                result["solution"] = candidate
                stop_flag.set()
                return True
            nonce += step
        return False

    with futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(worker, i, workers) for i in range(workers)]
        for _ in futures.as_completed(futs):
            if stop_flag.is_set():
                break
    return result["solution"]

def menu_loop(stub, client_id: int):
    while True:
        print("""
==== RPC Miner Client ====
1) getTransactionID
2) getChallenge
3) getTransactionStatus
4) getWinner
5) getSolution
6) Mine (auto)
0) Exit
""")
        try:
            choice = int(input("Select: ").strip())
        except Exception:
            print("Invalid input.")
            continue

        if choice == 0:
            break
        elif choice == 1:
            tid = stub.GetTransactionID(pb2.Empty()).transaction_id
            print(f"Current transaction ID: {tid}")
        elif choice == 2:
            tid = int(input("transactionID: "))
            chal = stub.GetChallenge(pb2.TransactionIDRequest(transaction_id=tid)).challenge
            print(f"Challenge for {tid}: {chal}")
        elif choice == 3:
            tid = int(input("transactionID: "))
            st = stub.GetTransactionStatus(pb2.TransactionIDRequest(transaction_id=tid)).status
            print(f"Status for {tid}: {st} (1=pending,0=solved,-1=invalid)")
        elif choice == 4:
            tid = int(input("transactionID: "))
            w = stub.GetWinner(pb2.TransactionIDRequest(transaction_id=tid)).client_id
            print(f"Winner for {tid}: {w}")
        elif choice == 5:
            tid = int(input("transactionID: "))
            sol = stub.GetSolution(pb2.TransactionIDRequest(transaction_id=tid))
            print(f"Solution for {tid}: status={sol.status}, challenge={sol.challenge}, solution='{sol.solution}'")
        elif choice == 6:
            t0 = time.time()
            tid = stub.GetTransactionID(pb2.Empty()).transaction_id
            chal = stub.GetChallenge(pb2.TransactionIDRequest(transaction_id=tid)).challenge
            print(f"[mine] transaction={tid}, challenge={chal}")
            prefix = f"client{client_id}:tid{tid}"
            solution = mine_local(prefix, chal, max_seconds=120, workers=8)
            if solution is None:
                print("[mine] Gave up (timeout).");
                continue
            print(f"[mine] local solution: {solution}, sha1={hashlib.sha1(solution.encode()).hexdigest()}")
            resp = stub.SubmitChallenge(pb2.SubmitChallengeRequest(
                transaction_id=tid, client_id=client_id, solution=solution
            ))
            print(f"[mine] server response result={resp.result} (1=valid,0=invalid,2=already solved,-1=invalid tid)")
            print(f"[mine] elapsed {time.time()-t0:.2f}s")
        else:
            print("Unknown option.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--server", default="localhost:50051")
    ap.add_argument("--client-id", type=int, default=1)
    args = ap.parse_args()

    channel = grpc.insecure_channel(args.server)
    stub = pb2_grpc.MinerServiceStub(channel)
    print(f"Connected to {args.server} as client {args.client_id}")
    menu_loop(stub, args.client_id)

if __name__ == "__main__":
    main()
