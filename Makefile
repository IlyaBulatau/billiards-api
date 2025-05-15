up: 
	docker compose --env-file src/.env up

migrate:
	docker exec -it backend alembic upgrade head