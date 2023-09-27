pytest:
	poetry run pytest -vv -s --disable-warnings tests

format:
	poetry run black .

up:
	poetry run python main.py


# E203 - whitespace before ':' - конфликтует с black
# E501 - line too long - конфликтует с black (не игнорирует комменты)
# W503 - line break before binary operator - конфликтует с black
# F401 - imported but unused - неактуально для __init__ и main.py файлов
# PIE803 - prefer-logging-interpolation - lazy % форматирования в логах, особого смысла нет
# B008 - Do not perform function calls in argument defaults - мешает использовать Depends
# DUO125 - avoid "commands" module use - просто модуль назван так у нас для filebrowser
# DUO106 - insecure use of "os" module
flake: 
	poetry run flake8 --per-file-ignores="__init__.py:F401 main.py:F401" --ignore E203,E501,W503,PIE803,B008,DUO125,DUO106 src main.py


mypy:
	poetry run mypy --ignore-missing-imports --check-untyped-defs src main.py