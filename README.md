# SmartMonitor — gRPC x REST/JSON

Projeto acadêmico desenvolvido para a disciplina de **Computação Paralela e Distribuída**, com o objetivo de demonstrar, na prática, o funcionamento do **gRPC**, **Protocol Buffers**, chamadas RPC e **Streaming**, além de comparar seu desempenho com uma implementação equivalente utilizando **REST/JSON**.

O projeto simula um sistema distribuído de monitoramento de sensores, no qual um cliente consulta informações como temperatura, umidade, status e timestamp.

## Objetivos do projeto

Este projeto demonstra:

- definição de contratos com Protocol Buffers;
- geração automática de código a partir de arquivos `.proto`;
- comunicação cliente-servidor com gRPC;
- chamada Unary RPC;
- Server Streaming;
- implementação equivalente utilizando REST/JSON;
- comparação de latência;
- comparação do tamanho do payload;
- funcionamento de um sistema distribuído simples.

## Tecnologias utilizadas

- Python
- gRPC
- Protocol Buffers
- Flask
- Requests
- HTTP/2
- REST
- JSON

## Estrutura do projeto

```text
grpc-protobuf-seminario/
│
├── proto/
│   └── monitor.proto
│
├── generated/
│   ├── __init__.py
│   ├── monitor_pb2.py
│   └── monitor_pb2_grpc.py
│
├── grpc_server.py
├── grpc_client.py
│
├── rest_server.py
├── rest_client.py
│
├── benchmark.py
├── generate_stubs.py
│
├── requirements.txt
└── README.md
```

## Contrato Protocol Buffers

O arquivo principal do contrato está localizado em:

```text
proto/monitor.proto
```

Ele define o serviço:

```proto
service MonitorService {
  rpc GetSensorStatus(SensorRequest) returns (SensorData);

  rpc MonitorSensor(SensorRequest) returns (stream SensorData);
}
```

O projeto utiliza dois tipos de comunicação gRPC:

### Unary RPC

O cliente envia uma requisição e recebe uma única resposta.

Fluxo:

```text
Cliente → Requisição → Servidor
Cliente ← Resposta ← Servidor
```

No projeto, essa chamada é utilizada por:

```text
GetSensorStatus
```

### Server Streaming

O cliente envia uma única requisição e o servidor mantém a comunicação aberta, enviando várias respostas.

Fluxo:

```text
Cliente → Requisição → Servidor

Cliente ← Resposta 1
Cliente ← Resposta 2
Cliente ← Resposta 3
Cliente ← ...
```

No projeto, essa comunicação é utilizada por:

```text
MonitorSensor
```

O servidor envia atualizações periódicas dos dados do sensor.

## Instalação

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd grpc-protobuf-seminario
```

## 2. Criar ambiente virtual

No Windows:

```bash
python -m venv .venv
```

Ative o ambiente:

```bash
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Instalar dependências

```bash
python -m pip install -r requirements.txt
```

As principais dependências são:

```text
grpcio==1.85.3
grpcio-tools==1.85.3
protobuf
Flask
requests
```

É importante manter `grpcio` e `grpcio-tools` em versões compatíveis, pois os arquivos gerados pelo Protocol Buffers dependem da versão da biblioteca utilizada.

## Geração dos arquivos gRPC

O arquivo:

```text
proto/monitor.proto
```

é compilado utilizando o script:

```bash
python generate_stubs.py
```

Esse processo gera automaticamente:

```text
generated/monitor_pb2.py
generated/monitor_pb2_grpc.py
```

O arquivo `monitor_pb2.py` contém as classes relacionadas às mensagens Protocol Buffers.

O arquivo `monitor_pb2_grpc.py` contém as classes relacionadas ao serviço gRPC, incluindo os stubs utilizados pelo cliente.

Os arquivos da pasta `generated` são produzidos automaticamente e não devem ser editados manualmente.

## Executando o servidor gRPC

Abra um terminal com o ambiente virtual ativo e execute:

```bash
python grpc_server.py
```

O servidor será iniciado em:

```text
localhost:50051
```

Saída esperada:

```text
Servidor gRPC iniciado
Endereço: localhost:50051
```

Mantenha esse terminal aberto.

## Executando o cliente gRPC

Em outro terminal:

```bash
python grpc_client.py
```

O menu apresentará:

```text
1 - Consultar sensor (Unary RPC)
2 - Monitorar sensor (Streaming)
0 - Sair
```

### Testando Unary RPC

Escolha:

```text
1
```

Informe um sensor:

```text
1
```

Exemplo de resposta:

```text
--- RESPOSTA gRPC UNARY ---

Sensor:       1
Temperatura:  27.45 °C
Umidade:      62.30 %
Status:       NORMAL
Timestamp:    1760000000
```

### Testando Server Streaming

Escolha:

```text
2
```

Informe o sensor:

```text
1
```

O servidor enviará várias atualizações:

```text
[01] Sensor=1 | Temp=26.80 °C | Umidade=61.40% | Status=NORMAL
[02] Sensor=1 | Temp=27.31 °C | Umidade=63.22% | Status=NORMAL
[03] Sensor=1 | Temp=32.75 °C | Umidade=59.10% | Status=ALERTA
```

O cliente realiza apenas uma requisição, enquanto o servidor continua transmitindo os dados.

## Executando o servidor REST

Para realizar a comparação, o projeto também possui uma implementação equivalente utilizando Flask e JSON.

Abra outro terminal:

```bash
python rest_server.py
```

O servidor estará disponível em:

```text
http://127.0.0.1:5000
```

## Testando o cliente REST

Execute:

```bash
python rest_client.py
```

Informe o ID do sensor.

Exemplo:

```text
--- RESPOSTA REST/JSON ---

Sensor:       1
Temperatura:  28.20 °C
Umidade:      65.50 %
Status:       NORMAL
Timestamp:    1760000000
```

## Benchmark gRPC x REST

O arquivo:

```text
benchmark.py
```

realiza uma comparação experimental entre:

```text
gRPC + Protocol Buffers
```

e:

```text
REST + JSON
```

Antes de executar o benchmark, mantenha ativos:

```text
grpc_server.py
rest_server.py
```

Depois execute:

```bash
python benchmark.py
```

O benchmark realiza:

```text
1000 requisições gRPC
1000 requisições REST
```

e mede:

- latência média;
- latência mediana;
- latência mínima;
- latência máxima;
- tamanho médio do payload.

Exemplo de saída:

```text
--- gRPC / Protocol Buffers ---

Latência média:   X.XXX ms
Latência mediana: X.XXX ms
Latência mínima:  X.XXX ms
Latência máxima:  X.XXX ms
Payload médio:    XX bytes


--- REST / JSON ---

Latência média:   X.XXX ms
Latência mediana: X.XXX ms
Latência mínima:  X.XXX ms
Latência máxima:  X.XXX ms
Payload médio:    XX bytes
```

Os resultados dependem do hardware, sistema operacional, carga da máquina e condições de execução.

Por esse motivo, os valores obtidos não devem ser interpretados como resultados universais.

## gRPC x REST

O projeto permite observar algumas diferenças entre as duas abordagens.

| Característica | gRPC | REST |
|---|---|---|
| Serialização | Protocol Buffers | JSON |
| Representação | Binária | Textual |
| Contrato | `.proto` | Normalmente OpenAPI ou documentação |
| Streaming | Nativo | Não nativo no modelo REST tradicional |
| Tipagem | Forte | Depende da implementação |
| Transporte | HTTP/2 | Geralmente HTTP/1.1 ou HTTP/2 |
| Uso comum | Microsserviços internos | APIs públicas e web |

## Arquitetura simplificada

```text
                    ┌───────────────────┐
                    │      Cliente      │
                    └─────────┬─────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
              gRPC                        REST
                │                           │
       Protocol Buffers                   JSON
                │                           │
        localhost:50051             localhost:5000
                │                           │
        ┌───────▼────────┐          ┌──────▼───────┐
        │ Servidor gRPC  │          │ Servidor REST│
        └────────────────┘          └──────────────┘
```

## Fluxo da demonstração

A apresentação prática pode seguir a seguinte sequência:

```text
monitor.proto
     ↓
stubs gerados
     ↓
servidor gRPC
     ↓
cliente gRPC
     ↓
Unary RPC
     ↓
Server Streaming
     ↓
servidor REST
     ↓
benchmark
     ↓
comparação dos resultados
```

## Conclusão

O projeto demonstra como o gRPC permite estabelecer comunicação entre serviços distribuídos utilizando contratos fortemente tipados definidos por Protocol Buffers.

A implementação permite observar tanto o modelo tradicional de uma requisição e uma resposta quanto o uso de Streaming para transmissão contínua de informações.

A comparação com REST/JSON complementa a demonstração ao permitir a análise experimental de latência e tamanho das mensagens em um mesmo cenário.

O objetivo não é afirmar que uma tecnologia substitui a outra em todos os casos, mas demonstrar as características de cada abordagem e como gRPC pode ser utilizado em cenários que exigem comunicação eficiente entre microsserviços.
