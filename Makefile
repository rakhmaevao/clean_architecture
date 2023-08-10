pytest:
	poetry run pytest -vv -s --disable-warnings tests/test_application/test_project_reader.py 

format:
	poetry run black .

up:
	poetry run python main.py