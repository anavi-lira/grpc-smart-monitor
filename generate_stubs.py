from pathlib import Path
from grpc_tools import protoc

BASE_DIR = Path(__file__).resolve().parent
PROTO_DIR = BASE_DIR / "proto"
OUT_DIR = BASE_DIR / "generated"
PROTO_FILE = PROTO_DIR / "monitor.proto"

OUT_DIR.mkdir(exist_ok=True)

resultado = protoc.main([
    "grpc_tools.protoc",
    f"-I{PROTO_DIR}",
    f"--python_out={OUT_DIR}",
    f"--grpc_python_out={OUT_DIR}",
    str(PROTO_FILE),
])

if resultado != 0:
    raise SystemExit("Erro ao gerar os stubs gRPC.")

grpc_file = OUT_DIR / "monitor_pb2_grpc.py"

conteudo = grpc_file.read_text(encoding="utf-8")

conteudo = conteudo.replace(
    "import monitor_pb2 as monitor__pb2",
    "from . import monitor_pb2 as monitor__pb2",
)

grpc_file.write_text(
    conteudo,
    encoding="utf-8"
)

print("Stubs gerados com sucesso em ./generated")