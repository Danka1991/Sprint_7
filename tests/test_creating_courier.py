from generator import FakeData
from data import Responses
import pytest
import allure
from src.api.CourierApi import CourierApi
fake = FakeData()

class TestCourier():
    
    @allure.title("Проверка создания курьера")
    def test_creating_courier(self, new_courier_session):
        with allure.step("Получение ответа на создание курьера из фикстуры"):
            create_resp = new_courier_session['create_resp']
        with allure.step("Проверка успешного создания курьера"):
            assert create_resp.status_code == 201 and create_resp.json() == Responses.OK_TRUE

    @allure.title("Проверка,если создать пользователя с логином, который уже есть, возвращается ошибка")    
    def test_creating_courier_with_the_same_data(self, new_courier_session):
        with allure.step("Получение учетных данных существующего курьера"):
            courier_api = CourierApi()
            double_create_resp = courier_api.create(new_courier_session["credentials"])
        with allure.step("Проверка ошибки дублирования логина"):
            assert double_create_resp.status_code == 409 and double_create_resp.json() == Responses.COURIER_LOGIN_EXISTS_ALREADY
    
    @allure.title("Проверка, если одного из полей нет, запрос возвращает ошибку")
    @pytest.mark.parametrize("data", [ # Достаточно 2 проверки, т.к. firstName не обязательное поле, без firstName код ответа 201
        ({"password": fake.gen_pass(), "firstName": fake.gen_name()}),
        ({"login": fake.gen_login(), "firstName": fake.gen_name()}),
    ])
    def test_courier_creation_scenario_with_invalid_data(self, data):
        with allure.step("Попытка создания курьера без обязательного поля"):
            courier_api = CourierApi()
            create_resp = courier_api.create(data)
        with allure.step("Проверка ошибки создания"):
            assert create_resp.json() == Responses.COURIER_CREATION_FAILED