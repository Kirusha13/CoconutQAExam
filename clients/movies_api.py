from custom_requester.custom_requester import CustomRequester
from config.base_urls import MOVIES_BASE_URL

MOVIES = '/movies'

class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIES_BASE_URL)

    def get_all_movies(self, params=None, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=MOVIES,
            params=params,
            expected_status=expected_status,
            **kwargs
        )

    def get_movie_by_id(self, movie_id, params=None, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES}/{movie_id}",
            params=params,
            expected_status=expected_status,
            **kwargs
        )

    def create_movie(self, movie_data, params=None, expected_status=201, **kwargs):
        return self.send_request(
            method="POST",
            endpoint=MOVIES,
            data=movie_data,
            params=params,
            expected_status=expected_status,
            **kwargs
        )

    def edit_movie(self, movie_id, new_data, params=None, expected_status=200, **kwargs):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES}/{movie_id}",
            data=new_data,
            params=params,
            expected_status=expected_status,
            **kwargs
        )

    def delete_movie(self, movie_id, params=None, expected_status=200, **kwargs):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES}/{movie_id}",
            params=params,
            expected_status=expected_status,
            **kwargs
        )