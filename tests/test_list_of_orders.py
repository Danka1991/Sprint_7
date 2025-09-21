import allure
from src.api.OrderApi import OrderApi

class TestOrdersList():
    @allure.title('Получение списка заказов')
    def test_orders_list(self):
        with allure.step("Отправка запроса на получение списка заказов"):
            order_api = OrderApi()
            orders_list_resp = order_api.get_orders()
        with allure.step("Проверка успешного получения списка заказов"):
            assert orders_list_resp.status_code == 200 and 'orders' in orders_list_resp.json()