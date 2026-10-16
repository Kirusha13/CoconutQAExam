import requests, pytest
from models.base_models import RegisterUserResponse
from constants.roles import Roles
import datetime, allure
from pytest_check import check
from pytest_mock import mocker

class TestAuth:
    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        registered_user = RegisterUserResponse(**response.json())

        assert registered_user.email == test_user.email
        assert registered_user.id != '' 
        assert Roles.USER in registered_user.roles 

    def test_register_and_login_user(self, api_manager, registered_user):
        login_data = {
            "email": registered_user.email,
            "password": registered_user.password
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user.email

    @allure.title("Тест регистрации пользователя с помощью Mock")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("qa_name", "Ivan Petrovich")
    def test_register_user_mock(self, api_manager, test_user, mocker):
        with allure.step(" Мокаем метод register_user в auth_api"):
            mock_response = RegisterUserResponse(  # Фиктивный ответ
                    id = "id",
                    email = "email@email.com",
                    fullName = "fullName",
                    verified = True,
                    banned = False,
                    roles = [Roles.SUPER_ADMIN],
                    createdAt = str(datetime.datetime.now())
                )

            mocker.patch.object(
                api_manager.auth_api,  # Объект, который нужно замокать
                'register_user',       # Метод, который нужно замокать
                return_value=mock_response  # Фиктивный ответ
            )

        with allure.step("Вызываем метод, который должен быть замокан"):
            register_user_response = api_manager.auth_api.register_user(test_user)
        
        with allure.step("Проверяем, что ответ соответствует ожидаемому"):
            with allure.step("Проверка поля персональных данных"): #обратите внимание на вложенность allure.step
                with check:
                    #Строка ниже выдаст исклющение и но выполнение теста продолжится
                    check.equal(register_user_response.fullName, "INCORRECT_NAME", "НЕСОВПАДЕНИЕ fullName")
                    check.equal(register_user_response.email, mock_response.email)
            
            with allure.step("Проверка поля banned"):
                with check("Проверка поля banned"): #можно использовать вместо allure.step
                    check.equal(register_user_response.banned, mock_response.banned)