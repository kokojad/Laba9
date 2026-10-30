"""Модульные тесты класса Calculator (pytest, параметризация)."""
import pytest

from calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


# ------------------------------------------------------------------- add
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-2, -3, -5),
    (-5, 5, 0),
    (0, 0, 0),
    (10, 0, 10),
    (1_000_000, 2_000_000, 3_000_000),
])
def test_add_integers(calc, a, b, expected):
    assert calc.add(a, b) == expected


def test_add_floats(calc):
    assert calc.add(0.1, 0.2) == pytest.approx(0.3)


# -------------------------------------------------------------- subtract
@pytest.mark.parametrize("a, b, expected", [
    (5, 3, 2),
    (3, 5, -2),
    (-4, -4, 0),
    (0, 7, -7),
    (-1, 1, -2),
])
def test_subtract(calc, a, b, expected):
    assert calc.subtract(a, b) == expected


# -------------------------------------------------------------- multiply
@pytest.mark.parametrize("a, b, expected", [
    (3, 4, 12),
    (-3, 4, -12),
    (-3, -4, 12),
    (0, 99, 0),
    (1, 7, 7),
])
def test_multiply_integers(calc, a, b, expected):
    assert calc.multiply(a, b) == expected


def test_multiply_floats(calc):
    assert calc.multiply(2.5, 4) == pytest.approx(10.0)


# ---------------------------------------------------------------- divide
@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),
    (7, 2, 3.5),
    (-9, 3, -3),
    (-9, -3, 3),
    (0, 5, 0),
    (1, 3, pytest.approx(0.3333333333)),
])
def test_divide(calc, a, b, expected):
    assert calc.divide(a, b) == expected


@pytest.mark.parametrize("a", [1, -1, 0, 3.5])
@pytest.mark.parametrize("zero", [0, 0.0])
def test_divide_by_zero_raises_exception(calc, a, zero):
    with pytest.raises(ZeroDivisionError, match="Деление на ноль"):
        calc.divide(a, zero)


# --------------------------------------------------------- is_prime_number
@pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 97, 7919])
def test_prime_numbers(calc, n):
    assert calc.is_prime_number(n) is True


@pytest.mark.parametrize("n", [4, 6, 8, 9, 15, 25, 100, 7917])
def test_composite_numbers_are_not_prime(calc, n):
    assert calc.is_prime_number(n) is False


@pytest.mark.parametrize("n", [1, 0, -1, -7])
def test_numbers_less_than_two_are_not_prime(calc, n):
    assert calc.is_prime_number(n) is False


@pytest.mark.parametrize("value", [2.5, "7", None, True, [3]])
def test_is_prime_number_rejects_non_integers(calc, value):
    with pytest.raises(TypeError):
        calc.is_prime_number(value)
