import pytest, allure

@pytest.mark.db
class TestDB:
    def test_db_requests(self, db_helper, created_test_user):
        assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
        assert db_helper.user_exists_by_email("api1@gmail.com")

    @pytest.mark.movies
    def test_lifecycle_of_movie(self, super_admin, db_helper, new_movie):
        movie_id = None
        try:
            with allure.step("Проверка отсутсвия фильма в БД"):
                assert db_helper.get_movie_by_name(new_movie['name']) is None

            with allure.step("Создание и взятие фильма из БД"):
                movie_id = super_admin.api.movies_api.create_movie(movie_data=new_movie).json()['id']
                movie_from_db =  db_helper.get_movie_by_id(movie_id) 
                assert movie_from_db is not None
                assert movie_from_db.name == new_movie['name']

            with allure.step("Удаление фильма в конце выполнения теста"):
                super_admin.api.movies_api.delete_movie(movie_id)
                assert db_helper.get_movie_by_id(movie_id) is None
                movie_id = None
        finally:
            with allure.step("Повторное удаление фильма при неудачном удалении"):
                if movie_id is not None and db_helper.get_movie_by_id(movie_id) is not None:
                    super_admin.api.movies_api.delete_movie(movie_id)
                
