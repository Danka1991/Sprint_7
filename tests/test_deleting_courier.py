from data import Responses
import allure
from src.api.CourierApi import CourierApi

class TestDeletingCourier():
    @allure.title("Проверка удаления курьера") 
    def test_deleting_courier(self, new_courier_session):
        courier_api = CourierApi()
        with allure.step("Получение ID курьера из сессии"):
            id = new_courier_session["login_resp"].json()['id']
        with allure.step("Отправка запроса на удаление курьера"):
            delete_resp = courier_api.delete(id)
        with allure.step("Попытка авторизации удаленного курьера для проверки"):
            login_resp = courier_api.login(new_courier_session["credentials"]) # проверяем что курьера точно не осталось в системе
        with allure.step("Проверка успешного удаления и отсутствия курьера в системе"):
            assert delete_resp.status_code == 200 and delete_resp.json() == Responses.OK_TRUE and login_resp.json() == Responses.COURIER_NOT_FOUND

    @allure.title("Проверка удаления курьера без id") 
    def test_deleting_courier_without_id(self):
        with allure.step("Отправка запроса на удаление с пустым ID"):
            courier_api = CourierApi()
            delete_resp = courier_api.delete("")
        with allure.step("Проверка ошибки при отсутствии ID"):
            assert delete_resp.status_code == Responses.COURIER_ID_NOT_FOUND["code"] and delete_resp.json() == Responses.NOT_FOUND        

    @allure.title("Проверка удаления курьера c несуществующим id") 
    def test_deleting_courier_without_id(self):
        with allure.step("Отправка запроса на удаление с несуществующим ID"):
            courier_api = CourierApi()
            delete_resp = courier_api.delete(0)
        with allure.step("Проверка ошибки при несуществующем ID"):
            assert delete_resp.status_code == Responses.COURIER_ID_NOT_FOUND["code"] and delete_resp.json() == Responses.COURIER_ID_NOT_FOUND