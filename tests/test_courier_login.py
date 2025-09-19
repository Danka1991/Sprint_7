from data import Responses
import pytest
import allure
from generator import FakeData
from src.api.CourierApi import CourierApi

class TestCourierLogin():
    
    fake = FakeData()
    courier_api = CourierApi()

    @allure.title('Курьер может авторизоваться, успешный запрос возвращает id')
    def test_courier_login(self, new_courier_session):
        login_resp = new_courier_session['login_resp']
        assert login_resp.status_code == 200 and 'id' in login_resp.json()
    
    @allure.title('Проверка, что незарегистрированный пользователь не может войти в сиситему, появление ошибки')
    def test_unregistered_courier_cannot_login(self):
        courier_fake_data = self.fake.gen_fake_courier_data()
        login_resp = self.courier_api.login(courier_fake_data)
        assert login_resp.status_code == 404 and login_resp.json() == Responses.COURIER_NOT_FOUND

    @allure.title('Система вернёт ошибку, если в данных запроса указать неправильно логин или пароль')
    @pytest.mark.parametrize("response_expected, data", [ 
        (Responses.COURIER_NOT_FOUND, {"login": '0000000ef00000'}), # указываем неверный логин
        (Responses.COURIER_LOGIN_FAILED, {"login": ''}), # указываем пустой логин
        (Responses.COURIER_LOGIN_FAILED, {"login": None}), # в запросе авторизации удаляем поле login
        (Responses.COURIER_NOT_FOUND, {"password": '0000000ef00000'}), # указываем неверный пароль
        (Responses.COURIER_LOGIN_FAILED, {"password": ''}), # указываем пустой пароль
        (Responses.COURIER_LOGIN_FAILED, {"password": None}) # в запросе авторизации удаляем поле password - 
                                                            # данный тест не проходит, тк сервер не возвращает ожидаемый ответ с ошибкой (результат 504 Gateway time out)
    ])
    def test_courier_creation_scenario_with_invalid_logins(self, response_expected, data, new_courier_session):
        credentials = new_courier_session["credentials"]

        keys = list(credentials.keys())
        for key in keys:
            if key in data:
                if data[key] == None:
                    del credentials[key]
                else:
                    credentials[key] = data[key]

        login_resp = self.courier_api.login(credentials)
        
        assert login_resp.status_code == response_expected['code'] and login_resp.json() == response_expected
        
    
