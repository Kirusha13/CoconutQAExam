import faker, random

fake = faker.Faker()

class DataGenerator:

    @staticmethod
    def generate_random_password():
        return "".join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*', k=10))

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        return f"{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return fake.user_name()
