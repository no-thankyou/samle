start_server:
	$(shell poetry run python main.py)

migrate:
	$(shell poetry run alembic upgrade head)

make_migrations:
	$(shell poetry run alembic revision --autogenerate -m "$(title)")

generate_configs:
	cd config && cp env.example .env

lint:
	poetry run ruff --fix
