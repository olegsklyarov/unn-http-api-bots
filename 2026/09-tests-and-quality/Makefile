# .PHONY — цель не связана с файлом на диске; make всегда выполнит рецепт,
# даже если в каталоге случайно появится файл с таким именем.
.PHONY: run test test-all install format-check format lint lint-fix mypy

# Запуск бота: загрузить переменные из .env в окружение и стартовать пакет bot.
run:
	set -o allexport && \
	. ./.env && \
	exec uv run python -m bot

# Тесты: корень лекции (пакет bot) и tests/ (модуль mock) в PYTHONPATH.
test:
	PYTHONPATH=.:tests uv run python tests/test_mock_attributes.py
	PYTHONPATH=.:tests uv run python tests/test_mock_callable.py
	PYTHONPATH=.:tests uv run python tests/test_long_polling.py
	PYTHONPATH=.:tests uv run python tests/test_dispatch_persist_update.py
	PYTHONPATH=.:tests uv run python tests/test_dispatch_persist_user.py

# Все проверки без автофиксов: format-check, lint, mypy, test.
test-all: format-check lint mypy test

# Dev-зависимости (ruff, mypy) в .venv через uv.
install:
	uv sync --group dev

# Код стайл: проверка / автоисправление (ruff format).
format-check:
	uv run ruff format --check .

format:
	uv run ruff format .

# Линтер: проверка / автоисправление (ruff check).
lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .

# Проверка типов.
mypy:
	uv run mypy bot
