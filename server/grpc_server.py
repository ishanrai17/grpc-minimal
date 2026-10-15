from concurrent import futures

import grpc

import ping_v2_pb2
import ping_v2_pb2_grpc


class Pinger(ping_v2_pb2_grpc.PingerServicer):
    def Ping(self, request, context):
        return ping_v2_pb2.PingReply(payload=request.payload)

    def PingClientStream(self, request_iterator, context):
        count = sum(1 for _ in request_iterator)
        return ping_v2_pb2.PingReply(count=count.to_bytes(4, "big"))

    def PingServerStream(self, request, context):
        for _ in range(int.from_bytes(request.count, "big")):
            yield ping_v2_pb2.PingReply(payload=request.payload)


server = grpc.server(futures.ThreadPoolExecutor())
ping_v2_pb2_grpc.add_PingerServicer_to_server(Pinger(), server)
server.add_insecure_port("[::]:50051")
server.start()
server.wait_for_termination()
