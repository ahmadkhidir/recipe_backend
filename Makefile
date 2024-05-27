build-d:
	@echo "Building docker image"
	docker compose up --build -d

restart-d:
	@echo "Restarting docker container"
	docker compose restart