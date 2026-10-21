from playwright.sync_api import Page, expect
from utils.data_generator import DataGenerator
from datetime import datetime
import random

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

def test_use_locators(page: Page):
    page.goto('https://demoqa.com/webtables')

    page.locator('button:has-text("Add")').click()

    modal = page.locator('.modal-content')
    head = modal.locator('div.modal-title:has-text("Registration Form")')

    assert head.is_visible()

    first_name_locator = modal.locator('input[placeholder="First Name"]')
    last_name_locator = modal.locator('input[placeholder="Last Name"]')
    email_locator = modal.locator('input[placeholder="name@example.com"]')
    age_locator = modal.locator('input[placeholder="Age"]')
    salary_locator = modal.locator('input[placeholder="Salary"]')
    department_locator = modal.locator('input[placeholder="Department"]')

    first_name_locator.fill('Petya')
    last_name_locator.fill('Petrovich')
    email_locator.fill('petya@mail.com')
    age_locator.fill('18')
    salary_locator.fill('1000000')
    department_locator.fill('AQA')

    modal.locator('button:has-text("Submit")').click()

def test_filling_student_form(page: Page):
    text_footer = '© 2013-2026 TOOLSQA.COM | ALL RIGHTS RESERVED.'

    date_now = datetime.now().strftime('%d %b %Y')

    gender_selector = random.choice([
        "#gender-radio-1",
        "#gender-radio-2",
        "#gender-radio-3",
    ])

    hobby_selectors = [
        "#hobbies-checkbox-1",
        "#hobbies-checkbox-2",
        "#hobbies-checkbox-3",
    ]
    selected_hobbies = random.sample(hobby_selectors, k=2)

    states_and_cities = [
        ("NCR", ["Delhi", "Gurgaon", "Noida"]),
        ("Haryana", ["Karnal", "Panipat"]),
        ("Rajasthan", ["Jaipur", "Jaiselmer", "Udaipur"]),
    ]

    state, cities = random.choice(states_and_cities)
    city = random.choice(cities)

    page.goto('https://demoqa.com/automation-practice-form')

    page.fill('#firstName', DataGenerator.generate_random_name())
    
    page.fill('#lastName', DataGenerator.generate_random_name())
    
    page.fill('#userEmail', DataGenerator.generate_random_email())
    
    page.check(gender_selector)
    
    page.fill('#userNumber', DataGenerator.generate_random_number())
    
    assert page.locator('#dateOfBirthInput').get_attribute('value') == date_now
    
    page.fill("#subjectsInput", "Maths")
    page.get_by_text("Maths", exact=True).click()
    
    for hobby in selected_hobbies:
        page.check(hobby)
    
    page.fill('#currentAddress', DataGenerator.generate_random_description())
    
    page.locator("#state").click()
    page.get_by_text(state, exact=True).click()

    page.locator("#city").click()
    page.get_by_text(city, exact=True).click()

    page.locator("#submit").click()
        
    footer = page.locator(f'footer >> span:has-text("{text_footer}")')
    assert footer.text_content() == text_footer

def test_check_of_activity_radiobuttons(page: Page):
    page.goto('https://demoqa.com/radio-button')

    assert page.is_enabled("#yesRadio")
    assert page.is_enabled("#impressiveRadio")
    assert not page.is_enabled("#noRadio")

def test_check_of_visability_elements(page: Page):
    page.goto("https://demoqa.com/checkbox")

    home = page.get_by_text("Home", exact=True)
    desktop = page.get_by_text("Desktop", exact=True)

    assert home.is_visible()
    assert not desktop.is_visible()

    home_row = page.locator('[role="treeitem"]:has-text("Home")')
    home_row.locator(".rc-tree-switcher").click()

    assert desktop.is_visible()

def test_button_becomes_visible(page: Page):
    page.goto("https://demoqa.com/dynamic-properties")

    button = page.locator("#visibleAfter")

    assert not button.is_visible()

    page.wait_for_selector(
        "#visibleAfter",
        state="visible",
        timeout=6_000,
    )

    assert button.is_visible()

def test_expect(page: Page):
    page.goto("https://demoqa.com/radio-button")

    yes = page.locator("#yesRadio")
    impressive = page.locator("#impressiveRadio")
    no = page.locator("#noRadio")

    expect(no).to_be_disabled()
    expect(yes).to_be_enabled()
    expect(impressive).to_be_enabled()

    yes.check()

    expect(yes).to_be_checked()
    expect(impressive).not_to_be_checked()
