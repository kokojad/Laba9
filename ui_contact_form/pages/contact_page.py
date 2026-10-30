"""Page Object страницы «Обратная связь»."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

FIELDS = ("name", "email", "phone", "subject", "message", "consent")


class ContactPage(BasePage):
    # --- локаторы (только стабильные id) ---
    FORM = (By.ID, "contact-form")
    NAME = (By.ID, "name")
    EMAIL = (By.ID, "email")
    PHONE = (By.ID, "phone")
    SUBJECT = (By.ID, "subject")
    MESSAGE = (By.ID, "message")
    CONSENT = (By.ID, "consent")
    SUBMIT = (By.ID, "submit-btn")
    SUCCESS = (By.ID, "success-message")

    @staticmethod
    def error_locator(field: str):
        return (By.ID, f"error-{field}")

    # --- действия ---
    def open_page(self):
        self.open("/")
        self.wait_visible(self.FORM)
        return self

    def fill_form(self, name=None, email=None, phone=None, subject=None, message=None, consent=None):
        """Заполняет только переданные поля (None — поле не трогаем)."""
        if name is not None:
            self.type_text(self.NAME, name)
        if email is not None:
            self.type_text(self.EMAIL, email)
        if phone is not None:
            self.type_text(self.PHONE, phone)
        if subject is not None:
            self.select_by_value(self.SUBJECT, subject)
        if message is not None:
            self.type_text(self.MESSAGE, message)
        if consent is not None:
            self.set_checkbox(self.CONSENT, consent)
        return self

    def submit(self):
        self.click(self.SUBMIT)
        return self

    # --- состояние страницы ---
    def error_text(self, field: str) -> str:
        return self.text_of(self.error_locator(field))

    def visible_errors(self) -> dict:
        """Словарь {поле: текст ошибки} для всех полей с непустой ошибкой."""
        errors = {f: self.error_text(f) for f in FIELDS}
        return {f: t for f, t in errors.items() if t}

    def is_success_shown(self) -> bool:
        return self.is_visible(self.SUCCESS)

    def success_text(self) -> str:
        return self.wait_visible(self.SUCCESS).text
