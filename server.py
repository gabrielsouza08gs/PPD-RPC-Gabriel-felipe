
import os
import random
import threading
from concurrent import futures
from datetime import datetime

import grpc
import hashlib

import grpcCalc_pb2 as pb2
import grpcCalc_pb2_grpc as pb2_grpc

HOST = os.environ.get("MINER_HOST", "[::]")
PORT = int(os.environ.get("MINER_PORT", "50051"))
MAX_CHALLENGE = int(os.environ.get("MAX_CHALLENGE", "5"))
MIN_CHALLENGE = int(os.environ.get("MIN_CHALLENGE", "1"))

def sha1_hex(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()

def is_valid(solution: str, challenge: int) -> bool:
    return sha1_hex(solution).startswith("0" * max(0, challenge))

class MinerState:
    def __init__(self):
        self.table = {}
        self.current_tid = 0
        self.lock = threading.Lock()
        self._new_transaction(0)

    def _new_transaction(self, tid: int):
        challenge = random.randint(MIN_CHALLENGE, MAX_CHALLENGE)
        self.table[tid] = {
            "challenge": challenge,
            "solution": "",
            "winner": -1,
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        self.current_tid = tid

    def get_transaction_id(self) -> int:
        with self.lock:
            if self.table[self.current_tid]["winner"] != -1:
                self._new_transaction(self.current_tid + 1)
            return self.current_tid

    def get_challenge(self, tid: int) -> int:
        with self.lock:
            if tid in self.table:
                return self.table[tid]["challenge"]
            return -1

    def get_status(self, tid: int) -> int:
        with self.lock:
            if tid not in self.table:
                return -1
            return 1 if self.table[tid]["winner"] == -1 else 0

    def submit(self, tid: int, client_id: int, solution: str) -> int:
        with self.lock:
            if tid not in self.table:
                return -1
            row = self.table[tid]
            if row["winner"] != -1:
                return 2
            if is_valid(solution, row["challenge"]):
                row["solution"] = solution
                row["winner"] = client_id
                return 1
            else:
                return 0

    def winner(self, tid: int) -> int:
        with self.lock:
            if tid not in self.table:
                return -1
            if self.table[tid]["winner"] == -1:
                return 0
            return self.table[tid]["winner"]

    def solution(self, tid: int):
        with self.lock:
            if tid not in self.table:
                return (-1, "", -1)
            row = self.table[tid]
            status = 1 if row["winner"] == -1 else 0
            return (status, row["solution"], row["challenge"])

STATE = MinerState()

class MinerService(pb2_grpc.MinerServiceServicer):
    def GetTransactionID(self, request, context):
        return pb2.TransactionIDResponse(transaction_id=STATE.get_transaction_id())

    def GetChallenge(self, request, context):
        return pb2.ChallengeResponse(challenge=STATE.get_challenge(request.transaction_id))

    def GetTransactionStatus(self, request, context):
        return pb2.TransactionStatusResponse(status=STATE.get_status(request.transaction_id))

    def SubmitChallenge(self, request, context):
        result = STATE.submit(request.transaction_id, request.client_id, request.solution)
        return pb2.SubmitChallengeResponse(result=result)

    def GetWinner(self, request, context):
        return pb2.WinnerResponse(client_id=STATE.winner(request.transaction_id))

    def GetSolution(self, request, context):
        status, solution, challenge = STATE.solution(request.transaction_id)
        return pb2.SolutionResponse(status=status, solution=solution, challenge=challenge)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_MinerServiceServicer_to_server(MinerService(), server)
    server.add_insecure_port(f"{HOST}:{PORT}")
    print(f"[server] Listening on {HOST}:{PORT} (challenge {MIN_CHALLENGE}..{MAX_CHALLENGE})")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
