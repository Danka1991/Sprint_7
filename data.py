class Responses():
    OK_TRUE = {'ok': True}
    ORDER_NOT_FOUND = {"code":404,"message":"Заказ не найден"}
    NOT_ENOUGH_DATA_TO_FIND = {"code":400,"message":"Недостаточно данных для поиска"}
    NOT_FOUND = {"code":404,"message":"Not Found."}
    COURIER_ACCEPTING_ORDER_NOT_FOUND = {"code":404,"message":"Заказа с таким id не существует"}
    COURIER_ACCEPTING_COURIER_NOT_FOUND = {"code":404,"message":"Курьера с таким id не существует"}
    COURIER_ID_NOT_FOUND = {"code":404,"message":"Курьера с таким id нет."}
    COURIER_LOGIN_EXISTS_ALREADY = {'code': 409, 'message': 'Этот логин уже используется. Попробуйте другой.'}
    COURIER_CREATION_FAILED = {'code': 400, 'message': 'Недостаточно данных для создания учетной записи'}
    COURIER_LOGIN_FAILED = {'code': 400, 'message': 'Недостаточно данных для входа'}
    COURIER_NOT_FOUND = {"code":404,"message":"Учетная запись не найдена"}

    
test_order_data = [
    {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha"
    }
]