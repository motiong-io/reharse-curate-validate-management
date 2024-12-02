up:
	@alembic upgrade head
	@python app/main.py

migrate:
	@alembic upgrade head

test:
	@alembic upgrade head
	@clear
	@pytest -s --durations=0 -v 

format:
	@isort app/
	@isort tests/
	@black app/
	@black tests/