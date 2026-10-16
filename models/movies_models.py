from datetime import datetime
from pydantic import BaseModel

class Genre(BaseModel):
    name: str

class User(BaseModel):
    fullName: str

class Review(BaseModel):
    userId: str
    rating: int
    text: str
    createdAt: datetime
    user: User

class MovieResponse(BaseModel):

    id: int
    name: str
    price: int
    description: str
    imageUrl: str | None
    location: str
    published: bool
    genreId: int
    genre: Genre
    createdAt: datetime
    rating: float

class Movie(MovieResponse):
    reviews: list[Review]

class MoviesPage(BaseModel):

    movies: list[MovieResponse]
    count: int
    page: int 
    pageSize: int 
    pageCount: int