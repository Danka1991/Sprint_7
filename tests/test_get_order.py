from data import Responses, test_order_data
import allure
import pytest
from src.api.OrderApi import OrderApi

class TestGetOrder():
    
    order_api = OrderApi()

    @allure.title('Успешное получение заказа по треку')
    def test_get_order_by_track(self):
        order_resp = self.order_api.create_and_get_order(test_order_data[0])
        assert order_resp.status_code == 200 and 'order' in order_resp.json()

    @allure.title('Проверка получения заказа с неверными параметрами')
    @pytest.mark.parametrize("response_expected, params",[
        (Responses.ORDER_NOT_FOUND, {"t":0}), # указываем неверный track
        (Responses.NOT_ENOUGH_DATA_TO_FIND, {}), # запрос без track
    ])
    def test_get_order_by_wrong_track(self, response_expected, params):
        order_resp = self.order_api.get_order_by_track(params)
        assert order_resp.status_code == response_expected["code"] and order_resp.json() == response_expected
