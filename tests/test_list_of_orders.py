import allure
from src.api.OrderApi import OrderApi

class TestOrdersList():
    
    order_api = OrderApi()
    
    @allure.title('Получение списка заказов')
    def test_orders_list(self):
        orders_list_resp = self.order_api.get_orders()
        assert orders_list_resp.status_code == 200 and 'orders' in orders_list_resp.json()
