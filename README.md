# one-to-one

One Python client calling one Python server on Kind, measuring request latency over gRPC and plain HTTP.
`server/` and `client/` each have their own code, Dockerfile and Kubernetes manifest (`k8s.yaml`), and share the contract in `proto/ping_v2.proto` (all-`bytes` fields; `proto/ping.proto` is the unused v1).

- `server/grpc_server.py`: gRPC server on port 50051 (unary, client streaming, server streaming)
- `server/http_server.py`: HTTP/1.1 JSON server on port 8080 (unary only), a second container in the same pod
- `client/grpc_client.py`: `PingClient` for the gRPC server
- `client/http_client.py`: `HttpPingClient` for the HTTP server
- `client/bench.py`: `benchmark()` with a live tqdm progress bar, and `main()` that times gRPC vs HTTP

```sh
make up       # create the Kind cluster
make deploy   # build both images, load them into Kind, (re)start both pods
make client   # open a bash shell inside the client pod
make down     # delete the cluster
```

Inside the client pod, run `python`, then:

```python
from grpc_client import PingClient
from http_client import HttpPingClient
from bench import benchmark, main

c = PingClient()
c.unary()
c.client_stream()
c.server_stream()
benchmark("grpc unary", c.unary, 1_000)

h = HttpPingClient()
h.unary()
benchmark("http unary", h.unary, 1_000)

main(1_000)  # run every benchmark
```

Or from bash in the client pod: `python bench.py [calls]` (default 1,000).
