from playwright.sync_api import Page, expect
from utils.data_generator import DataGenerator

def test_registration(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')

    username_locator = '[data-qa-id="register_full_name_input"]'
    email_loacor = '[data-qa-id="register_email_input"]'
    password_locator = '[data-qa-id="register_password_input"]'
    repeat_password_locator = '[data-qa-id="register_password_repeat_input"]'

    user_name = DataGenerator.generate_random_name()
    user_password = DataGenerator.generate_random_password()
    user_email = f'test_{DataGenerator.generate_random_int(10000)}@email.qa'

    page.fill(username_locator, user_name)
    page.fill(email_loacor, user_email)
    page.fill(password_locator, user_password)
    page.fill(repeat_password_locator, user_password)

    page.click('[data-qa-id="register_submit_button"]')

    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)
