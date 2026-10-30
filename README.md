# Автотесты (ТПО, лабораторные работы 3–6)

![Run tests](../../actions/workflows/run-tests.yml/badge.svg)

Репозиторий содержит автотесты из лабораторных работ и workflow GitHub Actions, который запускает их при каждом
push и pull request.

| Папка | Что тестируется | Лабораторная работа |
|-------|-----------------|---------------------|
| `unit_tests/` | модульные тесты класса `Calculator` (pytest, параметризация) | ЛР №6 |
| `api_tests/` | REST API JSONPlaceholder (requests + pytest) | ЛР №5 |
| `ui_login/` | UI-тесты страницы логина (Selenium + pytest) | ЛР №3 |
| `ui_contact_form/` | UI-тесты контактной формы, Page Object, матрица решений | ЛР №4 |

## Локальный запуск

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows;  Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

cd unit_tests && pytest         # аналогично для api_tests, ui_login, ui_contact_form
```

UI-тесты по умолчанию запускаются в headless-режиме; ключ `--headed` показывает окно Chrome.

## CI

Workflow `.github/workflows/run-tests.yml`: ОС ubuntu-latest → Python 3.12 → `pip install -r requirements.txt` →
`pytest` для каждого набора тестов (матрица из четырёх заданий). Скриншоты UI-тестов загружаются как артефакты.
