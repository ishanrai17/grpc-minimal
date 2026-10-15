import sys
import time

from tqdm import tqdm

from grpc_client import N, PingClient
from http_client import HttpPingClient


def percentile(sorted_latencies, p):
    return sorted_latencies[len(sorted_latencies) * p // 100]


def benchmark(name, call, calls, msgs=1):
    for _ in range(100):
        call()
    latencies = []
    with tqdm(total=calls, desc=name, unit="call", leave=False) as bar:
        for i in range(calls):
            start = time.perf_counter()
            call()
            latencies.append((time.perf_counter() - start) * 1e6)
            bar.update()
            if i % 100 == 0:
                so_far = sorted(latencies)
                bar.set_postfix_str(f"p50 {percentile(so_far, 50):.0f} µs  p99 {percentile(so_far, 99):.0f} µs",
                                    refresh=False)
    total_ms = sum(latencies) / 1000
    latencies.sort()
    p50, p90, p99 = (percentile(latencies, p) for p in (50, 90, 99))
    print(f"{name:<20} total {total_ms:8.1f} ms  p50 {p50:7.0f} µs  p90 {p90:7.0f} µs  p99 {p99:7.0f} µs  "
          f"per-msg {p50 / msgs:6.1f} µs")


def main(calls=1_000):
    grpc_client = PingClient()
    http_client = HttpPingClient()
    # benchmark("grpc client_stream", grpc_client.client_stream, calls, N)
    # benchmark("grpc server_stream", grpc_client.server_stream, calls, N)
    benchmark("grpc unary", grpc_client.unary, calls)
    benchmark("http unary", http_client.unary, calls)
    grpc_client.close_channel()
    http_client.conn.close()


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1_000)
