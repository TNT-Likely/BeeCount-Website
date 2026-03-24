.PHONY: up down logs rebuild incremental test

up:
	docker compose up --build -d qdrant rag-api

down:
	docker compose down

logs:
	docker compose logs -f rag-api

rebuild:
	curl -X POST http://127.0.0.1:8008/v1/ingest/rebuild

incremental:
	curl -X POST http://127.0.0.1:8008/v1/ingest/incremental

test:
	pytest -q
