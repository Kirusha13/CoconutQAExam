from playwright.sync_api import expect
from utils.data_generator import DataGenerator
import allure, pytest

@allure.epic("Тестирование UI")
@allure.feature("Отзывы")
@pytest.mark.ui
class TestReview:
    @allure.title("Успешное создание отзыва на фильм")
    def test_review(self, common_user, login_page, movie_page, page):
        with page.expect_response(
            lambda response: (
                response.request.method == "POST"
                and response.url.endswith("/login")
            )
        ) as response_info:
            login_page.login(common_user.email, common_user.password)

        login_response = response_info.value
        assert login_response.status == 201

        page.get_by_text("Что-то пошло не так", exact=True).wait_for(state="visible")

        page.reload()

        expect(page).to_have_url("https://dev-cinescope.coconutqa.ru/")

        review_text = f"UI review {DataGenerator.generate_random_int(999999)}"
        movie_page.open()
        movie_page.create_review(
            text_review=review_text,
            rating=DataGenerator.generate_random_int(5)
        )
        expect(page.get_by_text(review_text, exact=True)).to_be_visible()
                