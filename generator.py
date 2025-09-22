from faker import Faker

class FakeData():
    faker = Faker()

    def gen_name(self):
        return self.faker.first_name()
    
    def gen_login(self):
        return self.faker.user_name()
    
    def gen_pass(self):
        return self.faker.random_number(10)
    
    def gen_fake_courier_data(self):
        return {
            "login": self.gen_login(),
            "password": self.gen_pass(),
            "firstName": self.gen_name()
        }