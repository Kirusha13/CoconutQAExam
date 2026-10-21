from models.base_models import TestUser as TestUserModel, RegisterUserResponse
import logging

logger = logging.getLogger(__name__)

class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)
        created_user = RegisterUserResponse(**response.json())

        assert created_user.email == creation_user_data.email
        assert created_user.fullName == creation_user_data.fullName
        assert created_user.roles == creation_user_data.roles
        assert created_user.verified is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        created_user = RegisterUserResponse(**created_user_response)
        response_by_id = super_admin.api.user_api.get_user_info(created_user.id).json()
        response_by_email = super_admin.api.user_api.get_user_info(created_user.email).json()
        
        user_by_id = RegisterUserResponse(**response_by_id)
        user_by_email = RegisterUserResponse(**response_by_email)

        assert user_by_id == user_by_email, "Содержание ответов должно быть идентичным"
        assert user_by_id.id and user_by_id.id != '', "ID должен быть не пустым"
        assert user_by_id.email == created_user.email
        assert user_by_id.fullName == created_user.fullName
        assert user_by_id.roles == created_user.roles
        assert user_by_id.verified is True

    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user_info(common_user.email, expected_status=403)