from curl import Urls  # первый вариант
import requests

class CourierApi():
    def create(self, data):
        return requests.post(Urls.create_courier, json=data)
    
    def login(self, data):
        return requests.post(Urls.login_courier, json=data)
    
    def delete(self, id):
        return requests.delete(Urls.delete_courier+str(id))