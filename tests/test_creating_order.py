from data import test_order_data
import pytest
import allure
from src.api.OrderApi import OrderApi

class TestCreatingOrder():
    
    order_api = OrderApi()
    
    @allure.title('Создание заказа')
    @pytest.mark.parametrize("test_order_data, color",[
        (test_order_data[0], {"color": ["BLACK"]}),
        (test_order_data[0], {"color": ["BLACK", "GREY"] }),
        (test_order_data[0], {"color": []}),
    ])
    def test_creating_order_with_dif_color_scooter(self, test_order_data, color):

        test_order_data = {**test_order_data, **color}
        create_order_resp = self.order_api.create(test_order_data)
        assert create_order_resp.status_code == 201 and "track" in create_order_resp.json()
