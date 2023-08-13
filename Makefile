pytest:
	poetry run pytest -vv -s --disable-warnings tests/test_application

format:
	poetry run black .

up:
	poetry run python main.py