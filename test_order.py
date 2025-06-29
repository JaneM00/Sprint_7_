# test_order.py
import requests
import pytest
from locators import BASE_URL, ORDERS_CREATE, ORDERS_LIST

class TestOrder:
    def get_sample_order_data(self):
        return {
            'firstName': 'Ivan',
            'lastName': 'Ivanov',
            'address': 'Lenina street',
            'metroStation': '4',
            'phone': '+79991112233',
            'rentTime': 5,
            'deliveryDate': '2023-10-10',
            'comment': '',
            'color': [],  # по умолчанию без цвета; можно менять в тестах.
            'price': 1000,
        }

    @pytest.mark.parametrize("colors", [
       [],
       ["BLACK"],
       ["GREY"],
       ["BLACK", "GREY"]
    ])
    def test_create_order_with_colors(self, colors):
        order_body = self.get_sample_order_data()
        order_body['color'] = colors if colors else None

        # Удаляем ключи со значением None
        order_body_cleaned = {k: v for k, v in order_body.items() if v is not None}

        response = requests.post(f"{BASE_URL}{ORDERS_CREATE}", json=order_body_cleaned)
        
        assert response.status_code in [200, 201]
        
        resp_json = response.json()
        
        # Проверка наличия track номера в ответе.
        assert isinstance(resp_json.get("track"), int)

    def test_get_orders(self):
        response = requests.get(f"{BASE_URL}{ORDERS_LIST}")
        assert response.status_code == 200
        orders_list = response.json()
        assert isinstance(orders_list, list)
