"""API-тесты JSONPlaceholder (ЛР №5): повторяют логику тестов коллекции Postman на requests + pytest."""
import re

import pytest

USER_ID = 1
TIMEOUT = 10
MAX_RESPONSE_TIME = 2.0  # секунды, как в Postman-тестах (2000 мс)


# ------------------------------------------------------------------ GET
@pytest.fixture(scope="module")
def get_response(session, base_url):
    return session.get(f"{base_url}/users/{USER_ID}", timeout=TIMEOUT)


def test_get_status_code_is_200(get_response):
    assert get_response.status_code == 200


def test_get_content_type_is_json(get_response):
    assert "application/json" in get_response.headers["Content-Type"]


def test_get_response_time_is_below_limit(get_response):
    assert get_response.elapsed.total_seconds() < MAX_RESPONSE_TIME


def test_get_json_has_expected_structure(get_response):
    user = get_response.json()
    assert set(user) == {"id", "name", "username", "email", "address", "phone", "website", "company"}
    assert set(user["address"]) == {"street", "suite", "city", "zipcode", "geo"}
    assert set(user["address"]["geo"]) == {"lat", "lng"}
    assert set(user["company"]) == {"name", "catchPhrase", "bs"}


def test_get_field_types_are_correct(get_response):
    user = get_response.json()
    assert isinstance(user["id"], int)
    assert isinstance(user["name"], str) and user["name"]
    assert isinstance(user["username"], str)
    assert isinstance(user["email"], str)


def test_get_user_id_equals_requested_id(get_response):
    assert get_response.json()["id"] == USER_ID


def test_get_email_has_valid_format(get_response):
    assert re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", get_response.json()["email"])


def test_get_known_values_of_user_1(get_response):
    user = get_response.json()
    assert user["name"] == "Leanne Graham"
    assert user["username"] == "Bret"


# ------------------------------------------------------------------ POST
NEW_USER = {"name": "Ivan Petrov", "username": "ipetrov", "email": "ivan.petrov@example.com"}


@pytest.fixture(scope="module")
def post_response(session, base_url):
    return session.post(f"{base_url}/users", json=NEW_USER, timeout=TIMEOUT)


def test_post_status_code_is_201(post_response):
    assert post_response.status_code == 201


def test_post_content_type_is_json(post_response):
    assert "application/json" in post_response.headers["Content-Type"]


def test_post_response_contains_generated_numeric_id(post_response):
    created = post_response.json()
    assert "id" in created
    assert isinstance(created["id"], int)


def test_post_response_echoes_sent_fields(post_response):
    created = post_response.json()
    for field, value in NEW_USER.items():
        assert created[field] == value


def test_post_response_time_is_below_limit(post_response):
    assert post_response.elapsed.total_seconds() < MAX_RESPONSE_TIME


# ------------------------------------------------------------------ PUT
UPDATED_USER = {"id": USER_ID, "name": "Ivan Petrov (updated)", "username": "ipetrov",
                "email": "ivan.updated@example.com"}


@pytest.fixture(scope="module")
def put_response(session, base_url):
    return session.put(f"{base_url}/users/{USER_ID}", json=UPDATED_USER, timeout=TIMEOUT)


def test_put_status_code_is_200(put_response):
    assert put_response.status_code == 200


def test_put_resource_id_is_preserved(put_response):
    assert put_response.json()["id"] == USER_ID


def test_put_fields_are_updated(put_response):
    updated = put_response.json()
    assert updated["name"] == UPDATED_USER["name"]
    assert updated["email"] == UPDATED_USER["email"]


def test_put_json_structure_is_the_same_as_sent(put_response):
    assert set(put_response.json()) == {"id", "name", "username", "email"}


# -------------------------------------------------------------- негативный
def test_get_non_existing_user_returns_404(session, base_url):
    response = session.get(f"{base_url}/users/9999", timeout=TIMEOUT)

    assert response.status_code == 404
    assert response.json() == {}
