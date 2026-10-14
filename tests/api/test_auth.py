import requests, pytest
from models.base_models import RegisterUserResponse
from constants.roles import Roles

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
