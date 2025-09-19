from curl import Urls
import requests

class OrderApi():
    def create(self, order_data):
        return requests.post(Urls.order, json=order_data)
    
    def get_orders(self, params={}):
        return requests.get(Urls.order, params=params)
    
    def get_order_by_track(self, params):
        return requests.get(Urls.get_order_by_track, params=params)
    
    def assign_order_to_courier(self, order_id, params):
        return requests.put(Urls.order_accept + str(order_id), params=params)
    
    def create_and_get_order(self, order_data):
        create_order_resp = self.create(order_data)
        order_track = create_order_resp.json()["track"]
        return self.get_order_by_track({"t":order_track})