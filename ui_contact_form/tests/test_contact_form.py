"""UI-автотесты формы обратной связи (ЛР №4) на основе паттерна Page Object."""
import pytest

SUCCESS_TEXT = "Спасибо! Ваше сообщение отправлено."

VALID = dict(
    name="Иван Петров",
    email="ivan.petrov@example.com",
    phone="+7 900 123-45-67",
    subject="question",
    message="Здравствуйте! Подскажите, как оформить заказ.",
    consent=True,
)


# ---------------------------------------------------------------- позитивные
def test_submit_valid_form_shows_success_message(contact_page, shot):
    """Позитивный сценарий: все поля заполнены валидными данными."""
    contact_page.fill_form(**VALID)
    shot("form_filled")
    contact_page.submit()

    assert contact_page.success_text() == SUCCESS_TEXT
    assert not contact_page.is_visible(contact_page.FORM)
    assert contact_page.visible_errors() == {}
    shot("success")


def test_submit_with_only_required_fields_shows_success(contact_page):
    """Телефон необязателен: форма отправляется и без него."""
    contact_page.fill_form(**{**VALID, "phone": ""})
    contact_page.submit()

    assert contact_page.success_text() == SUCCESS_TEXT


@pytest.mark.parametrize("field, value", [
    ("name", "Ян"),                       # нижняя граница имени (2 символа)
    ("message", "а" * 10),                # нижняя граница сообщения
    ("message", "а" * 500),               # верхняя граница сообщения
    ("phone", "9001234567"),              # 10 цифр без форматирования
])
def test_boundary_values_are_accepted(contact_page, field, value):
    contact_page.fill_form(**{**VALID, field: value})
    contact_page.submit()

    assert contact_page.is_success_shown()


# ---------------------------------------------------------------- негативные
def test_empty_required_name_shows_error(contact_page, shot):
    """Негативный сценарий: обязательное поле «Имя» пустое."""
    contact_page.fill_form(**{**VALID, "name": ""})
    contact_page.submit()

    assert contact_page.error_text("name") == "Введите имя"
    assert not contact_page.is_success_shown()
    assert contact_page.visible_errors() == {"name": "Введите имя"}
    shot("error_empty_name")


@pytest.mark.parametrize("field, value, error_field, expected_error", [
    ("name", "А", "name", "Имя должно содержать не менее 2 символов"),
    ("name", "Иван123", "name", "Имя может содержать только буквы"),
    ("email", "", "email", "Введите email"),
    ("email", "ivan.petrov@", "email", "Введите корректный email"),
    ("email", "ivan@mail", "email", "Введите корректный email"),
    ("phone", "12345", "phone", "Введите корректный номер телефона"),
    ("phone", "abc-defg-hij", "phone", "Введите корректный номер телефона"),
    ("subject", "", "subject", "Выберите тему"),
    ("message", "", "message", "Введите сообщение"),
    ("message", "Коротко", "message", "Сообщение должно содержать не менее 10 символов"),
    ("message", "а" * 501, "message", "Сообщение не должно превышать 500 символов"),
    ("consent", False, "consent", "Необходимо согласие на обработку данных"),
])
def test_invalid_field_shows_error(contact_page, field, value, error_field, expected_error):
    contact_page.fill_form(**{**VALID, field: value})
    contact_page.submit()

    assert contact_page.visible_errors() == {error_field: expected_error}
    assert not contact_page.is_success_shown()


def test_empty_form_shows_errors_for_all_required_fields(contact_page, shot):
    contact_page.submit()

    assert set(contact_page.visible_errors()) == {"name", "email", "subject", "message", "consent"}
    assert "phone" not in contact_page.visible_errors()  # необязательное поле
    assert not contact_page.is_success_shown()
    shot("error_empty_form")
