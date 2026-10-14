import faker, random, datetime

fake = faker.Faker()

class DataGenerator:

    @staticmethod
    def generate_random_password():
        password = random.choices('abcdefghiklmnopqrstuvwzyx')
        password += random.choices('0123456789')
        password += random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8)
        return "".join(password)
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

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }
    
    @staticmethod
    def generate_random_int(max_value: int) -> int:
        return random.randint(1, max_value)
    
