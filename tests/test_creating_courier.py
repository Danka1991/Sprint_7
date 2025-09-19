from generator import FakeData
from data import Responses
import pytest
import allure
from src.api.CourierApi import CourierApi

class TestCourier():
    
    courier_api = CourierApi()
    fake = FakeData()

    @allure.title("Проверка создания курьера")
    def test_creating_courier(self, new_courier_session):
        create_resp = new_courier_session['create_resp']
        assert create_resp.status_code == 201 and create_resp.json() == Responses.OK_TRUE

    @allure.title("Проверка,если создать пользователя с логином, который уже есть, возвращается ошибка")    
    def test_creating_courier_with_the_same_data(self, new_courier_session):
        double_create_resp = self.courier_api.create(new_courier_session["credentials"])
        assert double_create_resp.status_code == 409 and double_create_resp.json() == Responses.COURIER_LOGIN_EXISTS_ALREADY
    
    @allure.title("Проверка, если одного из полей нет, запрос возвращает ошибку")
    @pytest.mark.parametrize("data", [ # Достаточно 2 проверки, т.к. firstName не обязательное поле, без firstName код ответа 201
        ({"password": fake.gen_pass(), "firstName": fake.gen_name()}),
        ({"login": fake.gen_login(), "firstName": fake.gen_name()}),
    ])
    def test_courier_creation_scenario_with_invalid_data(self, data):
        create_resp = self.courier_api.create(data)
        assert create_resp.json() == Responses.COURIER_CREATION_FAILED