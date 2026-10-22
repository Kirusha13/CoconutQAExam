from pages.base_page import BasePage
import allure

class MoviePage(BasePage):
    def __init__(self, page, movie_id):
        super().__init__(page)
        self.url = f"{self.home_url}movies/{movie_id}"

        self.review_input = '[data-qa-id="movie_review_input"]'
        self.review_rating_button = 'button[role="combobox"]:has([data-qa-id="movie_rating_select"])'
        self.review_submit_button = '[data-qa-id="movie_review_submit_button"]'

    def open(self):
        self.open_url(self.url)

    def create_review(self, text_review: str, rating: int):
        self.enter_text(self.review_input, text_review)
        self.click(self.review_rating_button)
        with allure.step(f"Создать отзыв с оценкой {rating}"):
            self.page.get_by_role("option", name=f"{rating}", exact=True).click()
        self.click(self.review_submit_button)
