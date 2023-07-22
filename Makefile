test:
	poetry run pytest -vv -s --disable-warnings tests 

format:
	poetry run black .