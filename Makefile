up:
	docker-compose up --build

down:
	docker-compose down

test:
	pytest

test-e2e:
	pytest tests/e2e/test_full_flow.py