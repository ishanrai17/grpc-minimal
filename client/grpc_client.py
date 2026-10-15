import grpc

import ping_v2_pb2
import ping_v2_pb2_grpc

TARGET = "ping-server:50051"
N = 100

class PingClient:
    def __init__(self, target=TARGET):
        self.channel = grpc.insecure_channel(target)
        grpc.channel_ready_future(self.channel).result(timeout=60)
        self.stub = ping_v2_pb2_grpc.PingerStub(self.channel)
        self.request = ping_v2_pb2.PingRequest(payload=b"x" * 64, count=N.to_bytes(4, "big"))

    def unary(self):
        return self.stub.Ping(self.request)

    def client_stream(self):
        return self.stub.PingClientStream(self.request for _ in range(N))

    def server_stream(self):
        return list(self.stub.PingServerStream(self.request))

    def close_channel(self):
        self.channel.close()
