import requests
import pytest
from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator
from resources.user_creds import SuperAdminCreds
from entities.user import User
from constants.roles import Roles
from models.base_models import TestUser, RegisterUserResponse
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper
from utils.ui_tools import Tools

DEFAULT_UI_TIMEOUT = 30000


@pytest.fixture(scope="class")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="class")
def api_manager(session):
    return ApiManager(session)

@pytest.fixture(scope="session")
def unauthenticated_api_manager():
    http_session = requests.Session()
    yield ApiManager(http_session)
    http_session.close()

@pytest.fixture(scope="function")
def test_user():
    password = DataGenerator.generate_random_password()
    return TestUser(
        email = DataGenerator.generate_random_email(),
        fullName = DataGenerator.generate_random_name(),
        password = password,
        passwordRepeat = password,
        roles = [Roles.USER]
    )

@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user).json()
    RegisterUserResponse(**response)
    return test_user

@pytest.fixture(scope='function')
def new_movie(genre_id):
    return {
        "name": DataGenerator.generate_random_name(),
        "imageUrl": DataGenerator.generate_random_image_url(),
        "price": DataGenerator.generate_random_price(),
        "description": DataGenerator.generate_random_description(),
        "location": DataGenerator.generate_random_location(),
        "published": DataGenerator.generate_random_boolean(),
        'genreId': genre_id
    }

@pytest.fixture(scope='function')
def editable_movie(super_admin,new_movie, genre_id):
    new_movie['genreId'] = genre_id
    response = super_admin.api.movies_api.create_movie(new_movie)
    created_movie = response.json()

    yield created_movie

    super_admin.api.movies_api.delete_movie(created_movie['id'])


@pytest.fixture(scope='class')
def genre_id(api_manager):
    genres = api_manager.genres_api.get_all_genres().json()
    assert genres
    genre_id = genres[0]['id']

    return genre_id

@pytest.fixture(scope='function')
def movie_for_delete(super_admin,new_movie, genre_id):
    new_movie['genreId'] = genre_id
    response = super_admin.api.movies_api.create_movie(new_movie)
    created_movie = response.json()

    return created_movie

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user: TestUser) -> TestUser:
    return test_user.model_copy(update={"verified": True, "banned": False})

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()
    admin_data = creation_user_data.model_copy(update={"email": DataGenerator.generate_random_email()})

    admin = User(
        admin_data.email,
        admin_data.password,
        [Roles.ADMIN.value],
        new_session)

    admin_id = super_admin.api.user_api.create_user(admin_data).json()['id']
    super_admin.api.user_api.edit_user(admin_id,{'roles': [Roles.ADMIN.value]})

    admin.api.auth_api.authenticate(admin.creds)
    return admin

@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    log_name = f"trace_{Tools.get_timestamp()}.zip"
    trace_path = Tools.files_dir('playwright_trace', log_name)
    context.tracing.stop(path=trace_path)
    context.close()

@pytest.fixture(scope="function") 
def page(context):
    page = context.new_page()
    yield page
    page.close() 