import json
import statistics
import time

import grpc
import requests

from generated import monitor_pb2
from generated import monitor_pb2_grpc


TOTAL_REQUISICOES = 1000

SENSOR_ID = 1

GRPC_HOST = (
    "localhost:50051"
)

REST_URL = (
    "http://127.0.0.1:5000/"
    f"sensor/{SENSOR_ID}"
)


def benchmark_grpc():

    canal = grpc.insecure_channel(
        GRPC_HOST
    )

    stub = (
        monitor_pb2_grpc
        .MonitorServiceStub(
            canal
        )
    )

    req = (
        monitor_pb2
        .SensorRequest(
            sensor_id=SENSOR_ID
        )
    )

    # Aquecimento
    for _ in range(10):
        stub.GetSensorStatus(req)

    tempos = []
    payloads = []

    for _ in range(
        TOTAL_REQUISICOES
    ):

        inicio = (
            time.perf_counter()
        )

        resposta = (
            stub.GetSensorStatus(
                req
            )
        )

        fim = (
            time.perf_counter()
        )

        tempos.append(
            (fim - inicio) * 1000
        )

        payloads.append(
            len(
                resposta
                .SerializeToString()
            )
        )

    canal.close()

    return {
        "latencia_media":
            statistics.mean(
                tempos
            ),

        "latencia_mediana":
            statistics.median(
                tempos
            ),

        "latencia_min":
            min(tempos),

        "latencia_max":
            max(tempos),

        "payload_medio":
            statistics.mean(
                payloads
            )
    }


def benchmark_rest():

    sessao = requests.Session()

    # Aquecimento
    for _ in range(10):

        resposta = sessao.get(
            REST_URL,
            timeout=5
        )

        resposta.raise_for_status()

    tempos = []
    payloads = []

    for _ in range(
        TOTAL_REQUISICOES
    ):

        inicio = (
            time.perf_counter()
        )

        resposta = sessao.get(
            REST_URL,
            timeout=5
        )

        resposta.raise_for_status()

        fim = (
            time.perf_counter()
        )

        tempos.append(
            (fim - inicio) * 1000
        )

        json_bytes = json.dumps(
            resposta.json(),
            separators=(",", ":"),
            ensure_ascii=False
        ).encode(
            "utf-8"
        )

        payloads.append(
            len(json_bytes)
        )

    sessao.close()

    return {
        "latencia_media":
            statistics.mean(
                tempos
            ),

        "latencia_mediana":
            statistics.median(
                tempos
            ),

        "latencia_min":
            min(tempos),

        "latencia_max":
            max(tempos),

        "payload_medio":
            statistics.mean(
                payloads
            )
    }


def imprimir(nome, resultado):

    print(
        f"\n--- {nome} ---"
    )

    print(
        "Latência média:   "
        f"{resultado['latencia_media']:.3f} ms"
    )

    print(
        "Latência mediana: "
        f"{resultado['latencia_mediana']:.3f} ms"
    )

    print(
        "Latência mínima:  "
        f"{resultado['latencia_min']:.3f} ms"
    )

    print(
        "Latência máxima:  "
        f"{resultado['latencia_max']:.3f} ms"
    )

    print(
        "Payload médio:    "
        f"{resultado['payload_medio']:.2f} bytes"
    )


def main():

    print(
        "Benchmark: "
        f"{TOTAL_REQUISICOES} "
        "requisições por implementação"
    )

    grpc_resultado = (
        benchmark_grpc()
    )

    rest_resultado = (
        benchmark_rest()
    )

    imprimir(
        "gRPC / Protocol Buffers",
        grpc_resultado
    )

    imprimir(
        "REST / JSON",
        rest_resultado
    )

    diferenca = (
        1
        - grpc_resultado[
            "payload_medio"
        ]
        / rest_resultado[
            "payload_medio"
        ]
    ) * 100

    if diferenca > 0:

        print(
            "\nPayload Protobuf "
            f"{diferenca:.2f}% menor "
            "que JSON."
        )

    else:

        print(
            "\nNeste teste, "
            "o Protobuf não ficou "
            "menor que JSON."
        )

    if (
        grpc_resultado[
            "latencia_media"
        ]
        <
        rest_resultado[
            "latencia_media"
        ]
    ):

        ganho = (
            1
            - grpc_resultado[
                "latencia_media"
            ]
            / rest_resultado[
                "latencia_media"
            ]
        ) * 100

        print(
            "Neste ambiente, "
            "gRPC apresentou "
            f"{ganho:.2f}% "
            "menos latência média."
        )

    else:

        aumento = (
            grpc_resultado[
                "latencia_media"
            ]
            / rest_resultado[
                "latencia_media"
            ]
            - 1
        ) * 100

        print(
            "Neste ambiente, "
            "gRPC apresentou "
            f"{aumento:.2f}% "
            "mais latência média."
        )

    print(
        "\nOs resultados representam "
        "este ambiente local e "
        "não são valores universais."
    )


if __name__ == "__main__":
    main()