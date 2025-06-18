up: 
	docker compose --env-file src/.env up

rebuild:
	docker compose --env-file src/.env up --build

migrate:
	docker exec -it backend alembic upgrade head

init_bucket:
	docker exec -it backend python3 -m cli.init_bucket

exec:
	docker exec -it backend bash