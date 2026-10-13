from utils.data_generator import DataGenerator

class TestMovies:
    def test_get_afisha_of_movies(self, api_manager):
        response = api_manager.movies_api.get_all_movies()
        response_data = response.json()

        assert isinstance(response_data, dict)
        assert response_data["page"] == 1
        assert response_data["pageSize"] == 10
        assert isinstance(response_data["movies"], list)
        assert isinstance(response_data["count"], int)
        assert isinstance(response_data["pageCount"], int)

    def test_filter_of_get_movies(self, api_manager, genre_id):

        response = api_manager.movies_api.get_all_movies({"genreId": genre_id})
        response_data = response.json()

        assert isinstance(response_data, dict)
        assert "movies" in response_data
        assert isinstance(response_data["movies"], list)
        movies = response_data['movies']
        assert movies
        for movie in movies:
            assert movie["genreId"] == genre_id

    def test_get_movie_by_id_success(self, api_manager):
        all_movies_response = api_manager.movies_api.get_all_movies()
        all_movies_response_data = all_movies_response.json()

        assert isinstance(all_movies_response_data, dict)
        assert "movies" in all_movies_response_data
        assert isinstance(all_movies_response_data["movies"], list)
        all_movies = all_movies_response_data['movies']
        assert all_movies
        movie_id = all_movies[0]['id']

        response = api_manager.movies_api.get_movie_by_id(movie_id)
        response_data = response.json()

        assert isinstance(response_data, dict)
        assert "id" in response_data
        assert response_data['id'] == movie_id
        assert {"name", "price", "description", "genreId", "id"} <= response_data.keys()

    def test_negative_get_movie_by_id(self, api_manager):
        api_manager.movies_api.get_movie_by_id(0, expected_status=404)

    def test_create_movie(self, super_admin, new_movie):
        movie_id = None
        try:
            response = super_admin.movies_api.create_movie(movie_data=new_movie)
            response_data = response.json()
            

            assert isinstance(response_data, dict)
            assert 'id' in response_data
            movie_id = response_data['id']
        
        
            response_new_movie = super_admin.movies_api.get_movie_by_id(response_data['id'])
            new_movie_get_data = response_new_movie.json()
            assert response_data['id'] == new_movie_get_data['id']
            assert new_movie['genreId'] == new_movie_get_data['genreId']
            assert new_movie['name'] == new_movie_get_data['name']

        finally:
            if movie_id is not None:
                super_admin.movies_api.delete_movie(movie_id)

    def test_create_duplicate(self, super_admin, new_movie):
        movie_id = None
        try:
            response = super_admin.movies_api.create_movie(movie_data=new_movie)
            response_data = response.json()
            assert isinstance(response_data, dict)
            assert 'id' in response_data
            movie_id = response_data['id']
            duplicate_response = super_admin.movies_api.create_movie(movie_data=new_movie, expected_status=409)


        finally:
            if movie_id is not None:
                super_admin.movies_api.delete_movie(movie_id)



    def test_edit_movie(self, super_admin, editable_movie):
        new_name = f"{editable_movie['name']}+1"
        new_price = DataGenerator.generate_random_price()
        movie_id = editable_movie['id']
        response = super_admin.movies_api.edit_movie(
            movie_id=movie_id,
            new_data={
                "name": new_name,
                "price": new_price,
                "published": not(editable_movie['published'])
            }
            )
        response_data = response.json()

        movie_data = super_admin.movies_api.get_movie_by_id(movie_id).json()


        assert isinstance(response_data, dict)
        assert response_data['id'] == movie_data['id']
        assert response_data['name'] == movie_data['name']
        assert response_data['price'] == movie_data['price']
        assert response_data['published'] == movie_data['published']

    def test_edit_movie_with_invalid_id(self, super_admin):
        response = super_admin.movies_api.edit_movie(
            movie_id=0,
            new_data={'name': 'new_name'},
            expected_status=404
            )


    def test_delete_movie(self, super_admin, movie_for_delete):
        movie_id = movie_for_delete['id']
        super_admin.movies_api.delete_movie(movie_id)

        super_admin.movies_api.get_movie_by_id(movie_id=movie_id, expected_status=404)

    def test_delete_movie_negative(self, super_admin):
        super_admin.movies_api.delete_movie(movie_id=0, expected_status=404)



        
        

        









        
        
