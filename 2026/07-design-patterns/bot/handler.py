"""Контракт обработчика update.

Паттерн Strategy: каждый конкретный Handler — своя стратегия обработки.
Абстрактный базовый класс: https://docs.python.org/3/library/abc.html
Strategy: https://refactoring.guru/ru/design-patterns/strategy
Enum: https://docs.python.org/3/library/enum.html
Диаграммы: ../ARCHITECTURE.md
Материалы лекции: ../README.md
"""

from abc import ABC, abstractmethod
from enum import Enum


class HandlerStatus(Enum):
    """Результат handle для цепочки Dispatcher.

    CONTINUE — идём к следующему handler'у.
    STOP — update обработан, цепочку прерываем.
    """

    CONTINUE = 1
    STOP = 2


class Handler(ABC):
    @abstractmethod
    def can_handle(self, update: dict) -> bool:
        """Подходит ли этот handler для данного Update."""

    @abstractmethod
    def handle(self, update: dict) -> HandlerStatus:
        """Обработать update и вернуть CONTINUE или STOP."""
