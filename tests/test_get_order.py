from data import Responses, test_order_data
import allure
import pytest
from src.api.OrderApi import OrderApi

class TestGetOrder():
    @allure.title('Успешное получение заказа по треку')
    def test_get_order_by_track(self):
        with allure.step("Создание заказа и получение данных"):
            order_api = OrderApi()
            order_resp = order_api.create_and_get_order(test_order_data[0])
        with allure.step("Проверка успешного получения данных заказа"):
            assert order_resp.status_code == 200 and 'order' in order_resp.json()

    @allure.title('Проверка получения заказа с неверными параметрами')
    @pytest.mark.parametrize("response_expected, params",[
        (Responses.ORDER_NOT_FOUND, {"t":0}), # указываем неверный track
        (Responses.NOT_ENOUGH_DATA_TO_FIND, {}), # запрос без track
    ])
    def test_get_order_by_wrong_track(self, response_expected, params):
        with allure.step("Отправка запроса с неверными параметрами"):
            order_api = OrderApi()
            order_resp = order_api.get_order_by_track(params)
        with allure.step("Проверка ожидаемой ошибки"):
            assert order_resp.status_code == response_expected["code"] and order_resp.json() == response_expected