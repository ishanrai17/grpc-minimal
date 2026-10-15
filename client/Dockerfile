FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir grpcio-tools==1.66.1 tqdm==4.66.5
COPY proto/ client/ ./
RUN python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. ping_v2.proto
CMD ["sleep", "infinity"]
