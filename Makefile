test:
	poetry run pytest -vv -s --disable-warnings tests 

format:
	poetry run black .

up:
	poetry run python main.py