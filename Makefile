.PHONY: up deploy client down

up:
	kind get clusters | grep -qx grpc-minimal || kind create cluster --name grpc-minimal

deploy: up
	docker build -t grpc-server:dev -f server/Dockerfile .
	docker build -t grpc-client:dev -f client/Dockerfile .
	kind load docker-image grpc-server:dev grpc-client:dev --name grpc-minimal
	kubectl apply -f server/k8s.yaml -f client/k8s.yaml
	kubectl rollout restart deploy/ping-server deploy/ping-client
	kubectl rollout status deploy/ping-server
	kubectl rollout status deploy/ping-client

client: deploy
	kubectl exec -it deploy/ping-client -- bash

down:
	kind delete cluster --name grpc-minimal
