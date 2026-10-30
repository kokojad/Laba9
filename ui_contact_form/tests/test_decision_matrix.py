"""Матрица принятия решений: все 2·2·3·2·2·2 = 96 комбинаций состояний полей формы (ЛР №4).

Для каждого поля выбран представитель класса эквивалентности «валидно» / «невалидно»
(для телефона добавлен класс «пусто» — поле необязательное). Ожидаемый результат вычисляется по модели:
форма отправляется тогда и только тогда, когда ни одно поле не невалидно, а ошибки показываются
ровно для невалидных полей.
"""
import itertools

import pytest

VALUES = {
    "name": {"valid": "Иван Петров", "invalid": ""},
    "email": {"valid": "ivan.petrov@example.com", "invalid": "ivan.petrov@"},
    "phone": {"valid": "+7 900 123-45-67", "empty": "", "invalid": "12ab"},
    "subject": {"valid": "feedback", "invalid": ""},
    "message": {"valid": "Здравствуйте! Подскажите, как оформить заказ.", "invalid": "Коротко"},
    "consent": {"valid": True, "invalid": False},
}
ERRORS = {
    "name": "Введите имя",
    "email": "Введите корректный email",
    "phone": "Введите корректный номер телефона",
    "subject": "Выберите тему",
    "message": "Сообщение должно содержать не менее 10 символов",
    "consent": "Необходимо согласие на обработку данных",
}
ORDER = list(VALUES)
COMBINATIONS = list(itertools.product(*(VALUES[f] for f in ORDER)))


def _id(states):
    short = {"valid": "V", "invalid": "I", "empty": "E"}
    return ",".join(f"{f}={short[s]}" for f, s in zip(ORDER, states))


@pytest.mark.parametrize("states", COMBINATIONS, ids=[_id(c) for c in COMBINATIONS])
def test_decision_matrix(contact_page, states):
    data = {f: VALUES[f][s] for f, s in zip(ORDER, states)}
    contact_page.fill_form(**data)
    contact_page.submit()

    expected_errors = {f: ERRORS[f] for f, s in zip(ORDER, states) if s == "invalid"}
    assert contact_page.visible_errors() == expected_errors
    assert contact_page.is_success_shown() == (not expected_errors)
