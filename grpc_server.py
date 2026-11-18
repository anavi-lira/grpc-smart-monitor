from concurrent import futures
import random
import time

import grpc

from generated import monitor_pb2
from generated import monitor_pb2_grpc


def gerar_dados_sensor(sensor_id: int):

    temperatura = round(
        random.uniform(20.0, 35.0),
        2
    )

    umidade = round(
        random.uniform(40.0, 85.0),
        2
    )

    status = (
        "ALERTA"
        if temperatura >= 32
        else "NORMAL"
    )

    return monitor_pb2.SensorData(
        sensor_id=sensor_id,
        temperatura=temperatura,
        umidade=umidade,
        status=status,
        timestamp=int(time.time()),
    )


class MonitorService(
    monitor_pb2_grpc.MonitorServiceServicer
):

    def GetSensorStatus(
        self,
        request,
        context
    ):

        print(
            f"[gRPC] Consulta unária recebida "
            f"para sensor {request.sensor_id}"
        )

        return gerar_dados_sensor(
            request.sensor_id
        )

    def MonitorSensor(
        self,
        request,
        context
    ):

        print(
            f"[gRPC] Streaming iniciado "
            f"para sensor {request.sensor_id}"
        )

        for _ in range(10):

            if not context.is_active():
                break

            yield gerar_dados_sensor(
                request.sensor_id
            )

            time.sleep(1)


def iniciar_servidor():

    servidor = grpc.server(
        futures.ThreadPoolExecutor(
            max_workers=10
        )
    )

    monitor_pb2_grpc \
        .add_MonitorServiceServicer_to_server(
            MonitorService(),
            servidor
        )

    servidor.add_insecure_port(
        "[::]:50051"
    )

    servidor.start()

    print("=" * 55)
    print(
        "Servidor gRPC iniciado "
        "em localhost:50051"
    )
    print("=" * 55)

    servidor.wait_for_termination()


if __name__ == "__main__":
    iniciar_servidor()