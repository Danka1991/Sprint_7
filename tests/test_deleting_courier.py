from generator import FakeData
from data import Responses
import allure
from src.api.CourierApi import CourierApi

class TestDeletingCourier():
    
    courier_api = CourierApi()

    @allure.title("Проверка удаления курьера") 
    def test_deleting_courier(self, new_courier_session):
        id = new_courier_session["login_resp"].json()['id']
        delete_resp = self.courier_api.delete(id)
        login_resp = self.courier_api.login(new_courier_session["credentials"]) # проверяем что курьера точно не осталось в системе
        assert delete_resp.status_code == 200 and delete_resp.json() == Responses.OK_TRUE and login_resp.json() == Responses.COURIER_NOT_FOUND

    @allure.title("Проверка удаления курьера без id") 
    def test_deleting_courier_without_id(self):
        delete_resp = self.courier_api.delete("")
        assert delete_resp.status_code == Responses.COURIER_ID_NOT_FOUND["code"] and delete_resp.json() == Responses.NOT_FOUND        

    @allure.title("Проверка удаления курьера c несуществующим id") 
    def test_deleting_courier_without_id(self):
        delete_resp = self.courier_api.delete(0)
        assert delete_resp.status_code == Responses.COURIER_ID_NOT_FOUND["code"] and delete_resp.json() == Responses.COURIER_ID_NOT_FOUND