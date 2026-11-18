import random
import time

from flask import Flask
from flask import jsonify


app = Flask(__name__)


def gerar_dados_sensor(sensor_id: int):

    temperatura = round(
        random.uniform(
            20.0,
            35.0
        ),
        2
    )

    umidade = round(
        random.uniform(
            40.0,
            85.0
        ),
        2
    )

    status = (
        "ALERTA"
        if temperatura >= 32
        else "NORMAL"
    )

    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "umidade": umidade,
        "status": status,
        "timestamp": int(
            time.time()
        ),
    }


@app.get(
    "/sensor/<int:sensor_id>"
)
def consultar_sensor(sensor_id):

    return jsonify(
        gerar_dados_sensor(
            sensor_id
        )
    )


@app.get("/health")
def health():

    return jsonify({
        "status": "ok"
    })


if __name__ == "__main__":

    print(
        "Servidor REST iniciado em "
        "http://127.0.0.1:5000"
    )

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=True
    )