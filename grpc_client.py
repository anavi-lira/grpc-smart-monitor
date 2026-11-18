import grpc

from generated import monitor_pb2
from generated import monitor_pb2_grpc


def chamada_unaria(stub):

    sensor_id = int(
        input(
            "Informe o ID do sensor: "
        )
    )

    resposta = stub.GetSensorStatus(
        monitor_pb2.SensorRequest(
            sensor_id=sensor_id
        )
    )

    print(
        "\n--- RESPOSTA gRPC UNARY ---"
    )

    print(
        f"Sensor:       "
        f"{resposta.sensor_id}"
    )

    print(
        f"Temperatura:  "
        f"{resposta.temperatura:.2f} °C"
    )

    print(
        f"Umidade:      "
        f"{resposta.umidade:.2f} %"
    )

    print(
        f"Status:       "
        f"{resposta.status}"
    )

    print(
        f"Timestamp:    "
        f"{resposta.timestamp}"
    )


def chamada_streaming(stub):

    sensor_id = int(
        input(
            "Informe o ID do sensor: "
        )
    )

    print(
        "\n--- SERVER STREAMING ---"
    )

    respostas = stub.MonitorSensor(
        monitor_pb2.SensorRequest(
            sensor_id=sensor_id
        )
    )

    for numero, resposta in enumerate(
        respostas,
        start=1
    ):

        print(
            f"[{numero:02}] "
            f"Sensor={resposta.sensor_id} | "
            f"Temp={resposta.temperatura:.2f} °C | "
            f"Umidade={resposta.umidade:.2f}% | "
            f"Status={resposta.status}"
        )


def main():

    canal = grpc.insecure_channel(
        "localhost:50051"
    )

    stub = (
        monitor_pb2_grpc
        .MonitorServiceStub(
            canal
        )
    )

    while True:

        print(
            "\n1 - Consultar sensor "
            "(Unary RPC)"
        )

        print(
            "2 - Monitorar sensor "
            "(Streaming)"
        )

        print(
            "0 - Sair"
        )

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        try:

            if opcao == "1":
                chamada_unaria(stub)

            elif opcao == "2":
                chamada_streaming(stub)

            elif opcao == "0":
                break

            else:
                print(
                    "Opção inválida."
                )

        except grpc.RpcError as erro:

            print(
                "Erro ao comunicar "
                "com o servidor gRPC:"
            )

            print(erro)


if __name__ == "__main__":
    main()