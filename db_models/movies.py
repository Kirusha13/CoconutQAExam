from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float, Text, Enum
from typing import Dict, Any
from db_models.base import Base

class MoviesDBModel(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)  
    name = Column(Text)  
    price = Column(Integer)  
    description = Column(Text)  
    image_url = Column(Text, nullable=True)  
    location = Column(Enum("MSK", "SPB", name="Location"))  
    published = Column(Boolean)  
    rating = Column(Float)  
    genre_id = Column(Integer)
    created_at = Column(DateTime)  

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'image_url': self.image_url,
            'location': self.location,
            'published': self.published,
            'rating': self.rating,
            'genre_id': self.genre_id,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f"<Movie(id='{self.id}', name='{self.name}')>"
