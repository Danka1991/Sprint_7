from data import Responses, test_order_data
import pytest
import allure
from src.api.OrderApi import OrderApi

class TestCourierAcceptOrder():

    order_api = OrderApi()
    
    @allure.title('Создание заказа, добавление курьера, присвоение заказа курьеру')
   
    def test_courier_accept_order(self, new_courier_session):
        get_order_resp = self.order_api.create_and_get_order(test_order_data[0])
        order_id = get_order_resp.json()["order"]["id"]
        courier_id = new_courier_session["login_resp"].json()['id']
        order_accept_resp = self.order_api.assign_order_to_courier(order_id, {"courierId" : courier_id})

        assert order_accept_resp.status_code == 200 and order_accept_resp.json() == Responses.OK_TRUE

    @allure.title('Проверка присвоения заказа с неверными параметрами')
    @pytest.mark.parametrize("response_expected, wrong_data",[
        (Responses.COURIER_ACCEPTING_ORDER_NOT_FOUND, {"order_id": -1}), # указываем неверный order_id
        (Responses.NOT_FOUND, {"order_id": ""}), # указываем пустой order_id
        (Responses.COURIER_ACCEPTING_COURIER_NOT_FOUND, {"courierId": -1}), # указываем неверный courierId
        (Responses.NOT_ENOUGH_DATA_TO_FIND, {"courierId": None}), # удаляем поле courierId
    ])
    def test_courier_accept_order_with_wrong_params(self, response_expected, wrong_data, new_courier_session):
            # для чистоты проверки использую настроящие id заказа и id курьера в системе, 
            # чтобы попеременно только 1 параметр в проверке был неверный или отсутствовал 
        get_order_resp = self.order_api.create_and_get_order(test_order_data[0])
        order_id = get_order_resp.json()["order"]["id"]
        courier_id = new_courier_session["login_resp"].json()['id']
        params = {}
        data = {
            "order_id" : order_id,
            "courierId" : courier_id
        }
        keys = list(data.keys())
        for key in keys:
            if key in wrong_data:
                if wrong_data[key] == None:
                    del data[key]
                else:
                    data[key] = wrong_data[key]

        order_id = data["order_id"]
        if "courierId" in data:
            params["courierId"] = data["courierId"]

        order_accept_resp = self.order_api.assign_order_to_courier(order_id, params)
        assert order_accept_resp.status_code == response_expected["code"] and order_accept_resp.json() == response_expected
