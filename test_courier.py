# test_courier.py
import requests
import pytest
from locators import BASE_URL, COURIER_REGISTER, COURIER_LOGIN

def generate_random_string(length=10):
    import string, random
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

@pytest.fixture
def create_courier():
    # Генерируем уникальные данные для курьера
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()
    data = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    # Создаем курьера
    response = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
    # Проверяем успешное создание
    assert response.status_code == 201 or response.status_code == 409  # 409 если уже существует
    return data

class TestCourier:
    def generate_courier_data(self):
        login = generate_random_string()
        password = generate_random_string()
        first_name = generate_random_string()
        return {
            "login": login,
            "password": password,
            "firstName": first_name
        }

    def test_create_courier_success(self):
        data = self.generate_courier_data()
        response = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    def test_create_duplicate_courier(self):
        data = self.generate_courier_data()
        resp1 = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
        assert resp1.status_code == 201 or resp1.status_code == 409

        # Попытка создать такого же курьера еще раз
        resp2 = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
        # Ожидаем ошибку (например, 409 Conflict)
        assert resp2.status_code != 201

    def test_create_courier_missing_fields(self):
        base_data = self.generate_courier_data()
        for field in ["login", "password", "firstName"]:
            data = base_data.copy()
            del data[field]
            response = requests.post(f"{BASE_URL}{COURIER_REGISTER}", json=data)
            # Ожидаем ошибку (например, 400 Bad Request)
            assert response.status_code != 201

    def test_authorize_success(self, create_courier):
        response = requests.post(f"{BASE_URL}{COURIER_LOGIN}", json={
            "login": create_courier["login"],
            "password": create_courier["password"]
        })
        assert response.status_code == 200
        resp_json = response.json()
        assert isinstance(resp_json.get("id"), int)

    def test_authorize_wrong_credentials(self, create_courier):
        response = requests.post(f"{BASE_URL}{COURIER_LOGIN}", json={
            "login": create_courier["login"],
            "password": create_courier["password"] + "_wrong"
        })
        # Ожидаем ошибку авторизации (например, 404 или другой статус)
        assert response.status_code != 200

    def test_authorize_missing_fields(self, create_courier):
       for field in ["login", "password"]:
           data = {
               "login": create_courier["login"],
               "password": create_courier["password"]
           }
           del data[field]
           response = requests.post(f"{BASE_URL}{COURIER_LOGIN}", json=data)
           # Ожидаем ошибку (например, 400 Bad Request)
           assert response.status_code != 200
