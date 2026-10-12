import requests
import pytest
from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator


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
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user).json()
    test_user["id"] = response["id"]
    return test_user

@pytest.fixture(scope='function')
def super_admin():
    http_session = requests.Session()
    api_manager = ApiManager(session=http_session)
    api_manager.auth_api.authenticate(("api1@gmail.com","asdqwe123Q"))

    yield api_manager
    http_session.close()

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
    response = super_admin.movies_api.create_movie(new_movie)
    created_movie = response.json()

    yield created_movie

    super_admin.movies_api.delete_movie(created_movie['id'])


@pytest.fixture(scope='class')
def genre_id(api_manager):
    genres = api_manager.genres_api.get_all_genres().json()
    assert genres
    genre_id = genres[0]['id']

    return genre_id

@pytest.fixture(scope='function')
def movie_for_delete(super_admin,new_movie, genre_id):
    new_movie['genreId'] = genre_id
    response = super_admin.movies_api.create_movie(new_movie)
    created_movie = response.json()

    return created_movie
