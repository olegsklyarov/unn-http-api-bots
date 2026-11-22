# Запуск: make
N = 500
EXPECTED = $(shell echo $$(($(N) * 2)))
BENCH = 5000

.PHONY: all race lock rps

all: race lock rps

race:
	@echo "Эксперимент 1. Гонка"
	@echo "Два процесса по $(N) инкрементов"
	python3 init.py json
	python3 inc_json.py $(N) & python3 inc_json.py $(N) & wait
	python3 show.py json "JSON без lock" $(EXPECTED)
	python3 init.py sqlite
	python3 inc_sqlite.py $(N) & python3 inc_sqlite.py $(N) & wait
	python3 show.py sqlite "SQLite" $(EXPECTED)

lock:
	@echo ""
	@echo "Эксперимент 2. File lock"
	python3 init.py json
	python3 inc_json_lock.py $(N) & python3 inc_json_lock.py $(N) & wait
	python3 show.py json "JSON с lock" $(EXPECTED)


rps:
	@echo ""
	@echo "RPS: один процесс, $(BENCH) инкрементов"
	@echo "PRAGMA journal_mode=WAL, synchronous=NORMAL"
	python3 init.py json
	python3 rps.py "JSON+lock" inc_json_lock.py $(BENCH)
	python3 init.py sqlite
	python3 rps.py "SQLite   " inc_sqlite.py $(BENCH)
