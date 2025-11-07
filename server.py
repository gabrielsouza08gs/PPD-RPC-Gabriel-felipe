
import grpc
from concurrent import futures

import grpc_calc_pb2 as pb2
import grpc_calc_pb2_grpc as pb2_grpc

class CalcService(pb2_grpc.CalcServiceServicer):
    def Compute(self, request, context):
        op = request.op
        a = request.a
        b = request.b

        if op == pb2.ADD:
            return pb2.ComputeResponse(result=a + b, err=0, err_msg="")
        elif op == pb2.SUB:
            return pb2.ComputeResponse(result=a - b, err=0, err_msg="")
        elif op == pb2.MUL:
            return pb2.ComputeResponse(result=a * b, err=0, err_msg="")
        elif op == pb2.DIV:
            if b == 0:
                return pb2.ComputeResponse(result=0.0, err=1, err_msg="Divisão por zero")
            return pb2.ComputeResponse(result=a / b, err=0, err_msg="")
        else:
            return pb2.ComputeResponse(result=0.0, err=-1, err_msg="Operação inválida")

def serve(port: int = 50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_CalcServiceServicer_to_server(CalcService(), server)
    server.add_insecure_port(f"[::]:{port}")
    print(f"[server] Calculadora RPC escutando em 0.0.0.0:{port}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    import os
    port = int(os.getenv("CALC_PORT", "50051"))  # permite configurar por variável
    serve(port)

