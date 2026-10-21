from utils.data_generator import DataGenerator
from models.movies_models import MoviesPage, MovieResponse, MovieDetailsResponse
import pytest, allure

@allure.feature("Тестирование фильмов")
@pytest.mark.movies
class TestMovies:
    @allure.title("Тест получения списка фильмов")
    @allure.description("Этот тест проверяет корректность полученного списка фильмов.")
    def test_get_afisha_of_movies(self, api_manager):
        with allure.step("Отправка, получение и обработка запроса списка фильмов"):
            response = api_manager.movies_api.get_all_movies()
            movies_page = MoviesPage(**response.json())

        with allure.step("Проверка корректности полученных данных"):
            assert movies_page.page == 1
            assert movies_page.pageSize == 10

    @allure.title("Тест получения списка фильмов, используя различные фильтры")
    @pytest.mark.parametrize(
        ('params', 'movie_check'),
        [
            pytest.param(
                lambda _: {'locations': ['MSK']},
                lambda movie, _: movie.location == 'MSK',
                id='location'
            ),
            pytest.param(
                lambda _: {'minPrice': 100, 'maxPrice': 500},
                lambda movie, _: 100 <= movie.price <= 500,
                id='price'
            ),
            pytest.param(
                lambda genre_id: {'genreId': genre_id},
                lambda movie, genre_id: movie.genreId == genre_id,
                id='genre'
            ),
            
        ])
    def test_filter_of_get_movies(self, api_manager, genre_id, params, movie_check):
        with allure.step("Отправка, получение и обработка запроса списка фильмов"):
            response = api_manager.movies_api.get_all_movies(params(genre_id))
            payload = response.json()
            movies_page = MoviesPage(**payload)

        with allure.step("Создание списка фильмов"):
            movies = movies_page.movies
            assert movies
        with allure.step("Перебор и проверка фильмов по фильтрам"):
            for movie in movies:
                assert movie_check(movie, genre_id)

    @allure.title("Тест получения данных о фильме по id")
    def test_get_movie_by_id_success(self, api_manager):
        with allure.step("Отправка, получение и обработка запроса списка фильмов"):
            movies_response = api_manager.movies_api.get_all_movies()
            movies_page = MoviesPage(**movies_response.json())

        with allure.step("Взятие id одного фильма из непустого спика"):
            all_movies = movies_page.movies
            assert all_movies
            movie_id = all_movies[0].id

        with allure.step("Отправка, получение и обработка запроса фильма"):
            response = api_manager.movies_api.get_movie_by_id(movie_id)
            movie = MovieResponse(**response.json())

        with allure.step("Проверка на взятие верного фильма"):
            assert movie.id == movie_id

    @allure.title("Негативный тест получения данных о несуществующем фильме по id")
    @pytest.mark.negative
    def test_negative_get_movie_by_id(self, api_manager):
        api_manager.movies_api.get_movie_by_id(0, expected_status=404)

    @allure.title("Тест создания фильма")
    def test_create_movie(self, super_admin, new_movie):
        movie_id = None
        with allure.step("Попытка создания и дальнейшего получения данных о фильме"):
            try:
                with allure.step("Получение и обработка запроса создания фильма"):
                    response = super_admin.api.movies_api.create_movie(movie_data=new_movie)
                    created_movie = MovieResponse(**response.json())

                    movie_id = created_movie.id
            
                with allure.step("Получение фильма по id"):
                    response_new_movie = super_admin.api.movies_api.get_movie_by_id(created_movie.id)
                    movie_from_get = MovieDetailsResponse(**response_new_movie.json())

                with allure.step("Проверка корректности полученных данных о фильме"):
                    assert created_movie.id == movie_from_get.id
                    assert new_movie['genreId'] == movie_from_get.genreId
                    assert new_movie['name'] == movie_from_get.name

            finally:
                with allure.step("Удаление фильма в конце выполнения теста"):
                    if movie_id is not None:
                        super_admin.api.movies_api.delete_movie(movie_id)

    @allure.title("Негативный тест создания дубликата фильма")
    @pytest.mark.negative
    def test_create_duplicate(self, super_admin, new_movie):
        movie_id = None
        try:
            with allure.step("Создание нового фильма"):
                response = super_admin.api.movies_api.create_movie(movie_data=new_movie)
                movie_id = MovieResponse(**response.json()).id
            with allure.step("Попытка создания дубликата фильма"):
                super_admin.api.movies_api.create_movie(movie_data=new_movie, expected_status=409)
        finally:
            with allure.step("Удаление фильма в конце выполнения теста"):
                if movie_id is not None:
                    super_admin.api.movies_api.delete_movie(movie_id)

    @allure.title("Тест изменения данных о фильме")
    def test_edit_movie(self, super_admin, editable_movie):
        with allure.step("Создание новых данных о фильме"):
            new_name = f"{editable_movie['name']}+1"
            new_price = DataGenerator.generate_random_price()
            movie_id = editable_movie['id']
        with allure.step("Изменение данных о фильме"):
            response = super_admin.api.movies_api.edit_movie(
                movie_id=movie_id,
                new_data={
                    "name": new_name,
                    "price": new_price,
                    "published": not(editable_movie['published'])
                }
                )
            edit_movie = MovieResponse(**response.json())

        with allure.step("Получение и сверка новых данных о фильме"):
            movie_data = super_admin.api.movies_api.get_movie_by_id(movie_id)
            movie_from_get = MovieDetailsResponse(**movie_data.json())

            assert edit_movie.id == movie_from_get.id
            assert edit_movie.name == movie_from_get.name
            assert edit_movie.price == movie_from_get.price
            assert edit_movie.published == movie_from_get.published

    @allure.title("Негативный тест изменения данных о несуществующем фильме")
    @pytest.mark.negative
    def test_edit_movie_with_invalid_id(self, super_admin):
        super_admin.api.movies_api.edit_movie(
            movie_id=0,
            new_data={'name': 'new_name'},
            expected_status=404
            )

    @allure.title("Негативный тест на создание фильма ОБЫЧНЫМ пользователем")
    @pytest.mark.negative
    def test_create_movie_by_common_user(self, common_user, new_movie):
        common_user.api.movies_api.create_movie(movie_data=new_movie, expected_status=403)

    @allure.title("Тест проверки удаления фильмов ролью SUPER_ADMIN")
    def test_delete_movie_by_super_admin(self, super_admin, movie_for_delete):
        movie_id = movie_for_delete['id']
        super_admin.api.movies_api.delete_movie(movie_id)
        super_admin.api.movies_api.get_movie_by_id(movie_id, expected_status=404)

    @allure.title("Тест проверки удаления фильмов пользователями разных ролей")
    @pytest.mark.parametrize(
        'role',
        [
            pytest.param("USER", marks=pytest.mark.negative, id='user'),
            pytest.param("ADMIN", marks=pytest.mark.negative, id='admin')
        ])
    def test_delete_movie_by_user_and_admin(self, role, common_user, admin, super_admin, movie_for_delete):
        movie_id = movie_for_delete['id']
        role_api = {"USER": common_user, "ADMIN": admin}[role]
        role_api.api.movies_api.delete_movie(movie_id,expected_status=403)
        super_admin.api.movies_api.delete_movie(movie_id)
        super_admin.api.movies_api.get_movie_by_id(movie_id, expected_status=404)
