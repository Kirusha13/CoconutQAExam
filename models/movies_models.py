from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal

class Genre(BaseModel):
    name: str

class ReviewUser(BaseModel):
    fullName: str

class Review(BaseModel):
    userId: str
    rating: int = Field(ge=1, le=5)
    text: str
    createdAt: datetime
    user: ReviewUser

class MovieResponse(BaseModel):

    id: int
    name: str
    price: int
    description: str
    imageUrl: str | None
    location: Literal['MSK', 'SPB']
    published: bool
    genreId: int
    genre: Genre
    createdAt: datetime
    rating: float = Field(ge=0, le=5) 

class MovieDetailsResponse(MovieResponse):
    reviews: list[Review]

class MoviesPage(BaseModel):

    movies: list[MovieResponse]
    count: int
    page: int 
    pageSize: int 
    pageCount: int