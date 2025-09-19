import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from generator import FakeData
from src.api.CourierApi import CourierApi
courier_api = CourierApi()
fake = FakeData()

@pytest.fixture
def new_courier_session():
    courier_fake_data = fake.gen_fake_courier_data()
    i = 0 
    create_resp = courier_api.create(courier_fake_data)

    while create_resp.status_code != 201 and i <= 5: # иногда генерируется логин который уже зарегистрирован в системе, поэтому если регистраци не удалась, пробуем еще
        courier_fake_data = fake.gen_fake_courier_data()
        create_resp = courier_api.create(courier_fake_data)
        i += 1  

    login_resp = courier_api.login(courier_fake_data)

    yield {
        "create_resp": create_resp, 
        "login_resp" : login_resp, 
        "credentials" : courier_fake_data
    }

    courier_api.delete(login_resp.json()['id'])