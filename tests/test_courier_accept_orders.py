from data import Responses, test_order_data
import allure
from src.api.OrderApi import OrderApi
import pytest

class TestCourierAcceptOrder():
    
    @allure.title('Создание заказа, добавление курьера, присвоение заказа курьеру')
   
    def test_courier_accept_order(self, new_courier_session):
        order_api = OrderApi()
        with allure.step("Создание заказа"):
            get_order_resp = order_api.create_and_get_order(test_order_data[0])
        with allure.step("Получение ID созданного заказа"):
            order_id = get_order_resp.json()["order"]["id"]
        with allure.step("Получение ID курьера"):
            courier_id = new_courier_session["login_resp"].json()['id']
        with allure.step("Присвоение заказа курьеру"):
            order_accept_resp = order_api.assign_order_to_courier(order_id, {"courierId" : courier_id})
        with allure.step("Проверка ответа"):
            assert order_accept_resp.status_code == 200 and order_accept_resp.json() == Responses.OK_TRUE

    @allure.title('Проверка присвоения заказа с неверными параметрами')
    @pytest.mark.parametrize("response_expected, order_id",[
        (Responses.COURIER_ACCEPTING_ORDER_NOT_FOUND, -1), # указываем неверный order_id
        (Responses.NOT_FOUND, ""), # указываем пустой order_id
    ])
    def test_courier_accept_order_with_wrong_params(self, response_expected, order_id, new_courier_session):
        order_api = OrderApi()
        with allure.step("Создание заказа"):
            get_order_resp = order_api.create_and_get_order(test_order_data[0])
        with allure.step("Получение ID созданного заказа"):
            order_id = get_order_resp.json()["order"]["id"]
        with allure.step("Получение ID курьера"):
            courier_id = new_courier_session["login_resp"].json()['id']
        with allure.step("Отправка запроса с неверными параметрами"):
            order_accept_resp = order_api.assign_order_to_courier(order_id, {"courierId" : courier_id})
        with allure.step("Проверка ответа с ошибкой"):
            assert order_accept_resp.status_code == response_expected["code"] and order_accept_resp.json() == response_expected

    @allure.title('Проверка присвоения заказа с неверными параметрами')
    @pytest.mark.parametrize("response_expected, params",[
        (Responses.COURIER_ACCEPTING_COURIER_NOT_FOUND, {"courierId": -1}), # указываем неверный courierId
        (Responses.NOT_ENOUGH_DATA_TO_FIND, {}), # удаляем поле courierId
    ])
    def test_courier_accept_order_with_wrong_params(self, response_expected, params, new_courier_session):
        order_api = OrderApi()
        with allure.step("Создание заказа"):
            get_order_resp = order_api.create_and_get_order(test_order_data[0])
        with allure.step("Получение ID созданного заказа"):
            order_id = get_order_resp.json()["order"]["id"]
        with allure.step("Отправка запроса с неверными параметрами"):
            order_accept_resp = order_api.assign_order_to_courier(order_id, params)
        with allure.step("Проверка ответа с ошибкой"):
            assert order_accept_resp.status_code == response_expected["code"] and order_accept_resp.json() == response_expected