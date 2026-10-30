"""Класс Calculator — объект модульного тестирования (ЛР №6)."""


class Calculator:
    """Простой калькулятор с бизнес-логикой: арифметика и проверка числа на простоту."""

    def add(self, a, b):
        """Возвращает сумму a + b."""
        return a + b

    def subtract(self, a, b):
        """Возвращает разность a - b."""
        return a - b

    def multiply(self, a, b):
        """Возвращает произведение a * b."""
        return a * b

    def divide(self, a, b):
        """Возвращает частное a / b; при b == 0 выбрасывает ZeroDivisionError."""
        if b == 0:
            raise ZeroDivisionError("Деление на ноль невозможно")
        return a / b

    def is_prime_number(self, n):
        """Проверяет, является ли целое число n простым.

        Простое число — натуральное число больше 1, делящееся только на 1 и на себя.
        Для не целых значений (включая bool) выбрасывает TypeError.
        """
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("Аргумент должен быть целым числом")
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        divisor = 3
        while divisor * divisor <= n:
            if n % divisor == 0:
                return False
            divisor += 2
        return True
