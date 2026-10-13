import faker, random

fake = faker.Faker()

class DataGenerator:

    @staticmethod
    def generate_random_password():
        return "".join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        return f"{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return fake.user_name()

    @staticmethod
    def generate_random_image_url():
        return fake.image_url()

    @staticmethod
    def generate_random_price():
        return fake.random_int(100,500)

    @staticmethod
    def generate_random_description():
        return fake.text(30)

    @staticmethod
    def generate_random_boolean():
        return fake.boolean()

    @staticmethod
    def generate_random_location():
        return random.choice(["MSK", "SPB"])
    
