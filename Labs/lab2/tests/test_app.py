import pytest


# ================================
# БЛОК 1: СТРАНИЦА "ПАРАМЕТРЫ URL"
# ================================

def test_request_params_page_status(client):
    """Страница параметров URL доступна"""
    response = client.get('/request-params/')
    assert response.status_code == 200


def test_request_params_empty(client):
    response = client.get('/request-params/')
    assert "Нет параметров" in response.text


def test_request_params_with_data(client):
    response = client.get('/request-params/?name=Иван&age=20&city=Москва')
    assert "name" in response.text
    assert "Иван" in response.text
    assert "age" in response.text
    assert "20" in response.text
    assert "city" in response.text
    assert "Москва" in response.text


def test_request_params_special_chars(client):
    response = client.get('/request-params/?q=hello%20world&tag=flask%2Bpython')
    assert "hello world" in response.text
    assert "flask+python" in response.text


# ====================================
# БЛОК 2: СТРАНИЦА "ЗАГОЛОВКИ ЗАПРОСА"
# ====================================

def test_request_headers_page_status(client):
    response = client.get('/request-headers/')
    assert response.status_code == 200


def test_request_headers_contains_user_agent(client):
    headers = {'User-Agent': 'Mozilla/5.0 Test Browser'}
    response = client.get('/request-headers/', headers=headers)
    assert "User-Agent" in response.text
    assert "Mozilla/5.0 Test Browser" in response.text


def test_request_headers_contains_host(client):
    response = client.get('/request-headers/')
    assert "Host" in response.text


# =========================
# БЛОК 3: СТРАНИЦА "COOKIE"
# =========================

def test_request_cookies_page_status(client):
    response = client.get('/request-cookies/')
    assert response.status_code == 200


def test_request_cookies_no_cookie(client):
    response = client.get('/request-cookies/')
    assert "Cookie не установлен" in response.text


# ==================================
# БЛОК 4: СТРАНИЦА "ПАРАМЕТРЫ ФОРМЫ"
# ==================================

def test_request_form_page_status(client):
    response = client.get('/request-form/')
    assert response.status_code == 200


def test_request_form_get_no_data(client):
    response = client.get('/request-form/')
    assert "Отправленные данные" not in response.text


def test_request_form_post_displays_data(client):
    data = {'name': 'Иван', 'email': 'ivan@example.com', 'message': 'Привет!'}
    response = client.post('/request-form/', data=data)
    assert "Иван" in response.text
    assert "ivan@example.com" in response.text
    assert "Привет!" in response.text


def test_request_form_post_empty_data(client):
    response = client.post('/request-form/', data={'name': '', 'email': ''})
    assert "name" in response.text
    assert "email" in response.text


# =====================================
# БЛОК 5: СТРАНИЦА "ВАЛИДАЦИЯ ТЕЛЕФОНА"
# =====================================

def test_phone_validator_page_status(client):
    response = client.get('/phone-validator/')
    assert response.status_code == 200


def test_phone_validator_valid_1(client):
    response = client.post('/phone-validator/', data={'phone': '8(123)4567590'})
    assert "8-123-456-75-90" in response.text


def test_phone_validator_valid_2(client):
    response = client.post('/phone-validator/', data={'phone': '123.456.75.90'})
    assert "8-123-456-75-90" in response.text


def test_phone_validator_valid_3(client):
    response = client.post('/phone-validator/', data={'phone': '89161728872'})
    assert "8-916-172-88-72" in response.text


def test_phone_validator_valid_4(client):
    response = client.post('/phone-validator/', data={'phone': '9161728872'})
    assert "8-916-172-88-72" in response.text


def test_phone_validator_wrong_digit_count(client):
    response = client.post('/phone-validator/', data={'phone': '+7 123 456 75 9'})
    assert "Неверное количество цифр" in response.text
    assert "is-invalid" in response.text


def test_phone_validator_invalid_symbols(client):
    response = client.post('/phone-validator/', data={'phone': 'abc123def'})
    assert "недопустимые символы" in response.text.lower()
    assert "is-invalid" in response.text