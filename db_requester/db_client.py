from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from resources.db_creds import DbCreds

USERNAME = DbCreds.DB_USER
PASSWORD = DbCreds.DB_PASSWORD
HOST = DbCreds.DB_HOST
PORT = DbCreds.DB_PORT
DATABASE_NAME = DbCreds.DB_NAME

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}",
    echo=False 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """Создает новую сессию БД"""
    return SessionLocal()