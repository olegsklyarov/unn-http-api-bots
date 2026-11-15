# .PHONY — цель не связана с файлом на диске; make всегда выполнит рецепт,
# даже если в каталоге случайно появится файл с таким именем.
.PHONY: run test install format-check format lint lint-fix mypy

# Запуск бота: загрузить переменные из .env в окружение и стартовать пакет bot.
run:
	set -o allexport && \
	. ./.env && \
	exec python3 -m bot

# Тесты: корень лекции (пакет bot) и tests/ (модуль mock) в PYTHONPATH.
test:
	PYTHONPATH=.:tests python3 tests/test_mock_attributes.py
	PYTHONPATH=.:tests python3 tests/test_mock_callable.py
	PYTHONPATH=.:tests python3 tests/test_long_polling.py
	PYTHONPATH=.:tests python3 tests/test_dispatch_persist_update.py
	PYTHONPATH=.:tests python3 tests/test_dispatch_persist_user.py

# Dev-зависимости (ruff, mypy) в .venv через uv.
install:
	uv sync --group dev

# Код стайл: проверка / автоисправление (ruff format).
format-check:
	.venv/bin/ruff format --check .

format:
	.venv/bin/ruff format .

# Линтер: проверка / автоисправление (ruff check).
lint:
	.venv/bin/ruff check .

lint-fix:
	.venv/bin/ruff check --fix .

# Проверка типов.
mypy:
	.venv/bin/mypy bot
