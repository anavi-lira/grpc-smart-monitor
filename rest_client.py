import requests


def main():

    sensor_id = int(
        input(
            "Informe o ID do sensor: "
        )
    )

    resposta = requests.get(
        f"http://127.0.0.1:5000/"
        f"sensor/{sensor_id}",
        timeout=5
    )

    resposta.raise_for_status()

    dados = resposta.json()

    print(
        "\n--- RESPOSTA REST/JSON ---"
    )

    print(
        f"Sensor:       "
        f"{dados['sensor_id']}"
    )

    print(
        f"Temperatura:  "
        f"{dados['temperatura']:.2f} °C"
    )

    print(
        f"Umidade:      "
        f"{dados['umidade']:.2f} %"
    )

    print(
        f"Status:       "
        f"{dados['status']}"
    )

    print(
        f"Timestamp:    "
        f"{dados['timestamp']}"
    )


if __name__ == "__main__":
    main()