# QA

Улучшаем качество кода:
- [x] добавить Black https://github.com/psf/black
- [x] добавить ruff https://github.com/astral-sh/ruff
- [ ] настроить github actions

## Code Quality Tools

### Black (Code Formatter)
```bash
# Format all Python files
source .venv/bin/activate && black bot/

# Check formatting without making changes
source .venv/bin/activate && black --check bot/
```

### Ruff (Linter)
```bash
# Check for linting issues
source .venv/bin/activate && ruff check bot/

# Auto-fix linting issues
source .venv/bin/activate && ruff check --fix bot/

# Format imports (similar to isort)
source .venv/bin/activate && ruff check --fix --select I bot/
```

Добавляем функциональные тесты
- [ ] добавляем pytest
- [ ] уменьшаем связность хэндлеров с инфраструктурой (переходим на интерфейсы)
- [ ] мокам функции, которые ходят в БД
- [ ] мокаем telegram api_client

