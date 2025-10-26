# QA

Улучшаем качество кода:
- [x] добавить Black https://github.com/psf/black
- [x] добавить ruff https://github.com/astral-sh/ruff
- [x] настроить github actions

## Code Quality Tools

### Black (Code Style Formatter)
```bash
# Format all Python files
source .venv/bin/activate && black bot/

# Check code style without making changes
source .venv/bin/activate && black --check bot/
```

### Ruff (Linter)
```bash
# Check for linting issues
source .venv/bin/activate && ruff check bot/

# Auto-fix linting issues
source .venv/bin/activate && ruff check --fix bot/
```

## GitHub Actions CI/CD

The project includes automated code quality checks that run on every commit and pull request:

- **Black code style check**: Ensures code follows consistent formatting and style
- **Ruff linting**: Checks for code quality issues and potential bugs
- **Python 3.13 support**: Tests against the latest Python version

The workflow file is located at `.github/workflows/ci.yml` and will automatically run when you:
- Push commits to `main` or `master` branches
- Create pull requests targeting `main` or `master` branches

### Workflow Features:
- ✅ Caches pip dependencies for faster builds
- ✅ Tests against Python 3.13
- ✅ Fails the build if code quality checks don't pass
- ✅ Provides clear feedback on code style and linting issues

Добавляем функциональные тесты
- [ ] добавляем pytest
- [ ] уменьшаем связность хэндлеров с инфраструктурой (переходим на интерфейсы)
- [ ] мокам функции, которые ходят в БД
- [ ] мокаем telegram api_client

