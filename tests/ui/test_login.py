from playwright.sync_api import expect
import allure, pytest

@allure.epic("Тестирование UI")
@allure.feature("Вход")
@pytest.mark.ui
class TestLogin:
    @allure.title("Успешный вход в аккаунт пользователя")
    def test_login(self, registered_user, login_page, page):
        login_page.login(registered_user.email, registered_user.password)

        expect(page).to_have_url('https://dev-cinescope.coconutqa.ru/')
