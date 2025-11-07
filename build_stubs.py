
import sys, subprocess
from pathlib import Path

proto = Path(__file__).with_name("grpc_calc.proto")

cmd = [
    sys.executable, "-m", "grpc_tools.protoc",
    f"--proto_path={proto.parent}",
    f"--python_out={proto.parent}",
    f"--grpc_python_out={proto.parent}",
    str(proto)
]
print("Running:", " ".join(cmd))
subprocess.check_call(cmd)
print("OK - Stubs gerados: grpc_calc_pb2.py, grpc_calc_pb2_grpc.py")
