from data import Responses
from generator import FakeData
import pytest
import allure
from src.api.CourierApi import CourierApi

class TestCourierLogin():
    
    @allure.title('Курьер может авторизоваться, успешный запрос возвращает id')
    def test_courier_login(self, new_courier_session):
        with allure.step("Получение ответа на авторизацию из фикстуры"):
            login_resp = new_courier_session['login_resp']
        with allure.step("Проверка успешной авторизации и наличия id в ответе"):
            assert login_resp.status_code == 200 and 'id' in login_resp.json()
    
    @allure.title('Проверка, что незарегистрированный пользователь не может войти в сиситему, появление ошибки')
    def test_unregistered_courier_cannot_login(self):
        with allure.step("Генерация фейковых данных курьера"):
            fake = FakeData()
            courier_fake_data = fake.gen_fake_courier_data()
        with allure.step("Попытка авторизации с несуществующими данными"):
            courier_api = CourierApi()
            login_resp = courier_api.login(courier_fake_data)
        with allure.step("Проверка ошибки авторизации"):
            assert login_resp.status_code == 404 and login_resp.json() == Responses.COURIER_NOT_FOUND

    @allure.title('Система вернёт ошибку при неверном логине')
    @pytest.mark.parametrize("login_value, expected_response", [
        ("0000000ef00000", Responses.COURIER_NOT_FOUND),
        ("", Responses.COURIER_LOGIN_FAILED),
    ])
    def test_courier_login_with_invalid_login(self, login_value, expected_response, new_courier_session):
        with allure.step("Попытка авторизации с неверным логином"):
            credentials = new_courier_session["credentials"].copy()
            credentials["login"] = login_value
            courier_api = CourierApi()
            login_resp = courier_api.login(credentials)
        
        with allure.step("Проверка ожидаемой ошибки"):
            assert login_resp.status_code == expected_response["code"] \
            and login_resp.json() == expected_response

    @allure.title('Система вернёт ошибку при неверном пароле')
    @pytest.mark.parametrize("password_value, expected_response", [
        ("0000000ef00000", Responses.COURIER_NOT_FOUND),
        ("", Responses.COURIER_LOGIN_FAILED),
    ])
    def test_courier_login_with_invalid_password(self, password_value, expected_response, new_courier_session):
        with allure.step("Попытка авторизации с неверным паролем"):
            credentials = new_courier_session["credentials"].copy()
            credentials["password"] = password_value
            courier_api = CourierApi()
            login_resp = courier_api.login(credentials)
        
        with allure.step("Проверка ожидаемой ошибки"):
            assert login_resp.status_code == expected_response["code"] \
            and login_resp.json() == expected_response

    @allure.title('Система вернёт ошибку при отсутствии обязательных полей')
    @pytest.mark.parametrize("field_to_remove, expected_response", [
        ("login", Responses.COURIER_LOGIN_FAILED),
        ("password", Responses.COURIER_LOGIN_FAILED), # при удалении поля "Пароль" система не может обработать запрос и выдать правильную ошибку, вместо этого просто завситает
    ])
    def test_courier_login_with_missing_fields(self, field_to_remove, expected_response, new_courier_session):
        credentials = new_courier_session["credentials"].copy()
        courier_api = CourierApi()
        
        with allure.step(f"Удаление поля {field_to_remove}"):
            del credentials[field_to_remove]
        
        with allure.step("Попытка авторизации без обязательного поля"):
            login_resp = courier_api.login(credentials)
        
        with allure.step("Проверка ожидаемой ошибки"):
            assert login_resp.status_code == expected_response["code"] \
            and login_resp.json() == expected_response