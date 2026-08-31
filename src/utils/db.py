from sqlalchemy import create_engine
from src.utils.settings import app_settings
from sqlalchemy.orm import DeclarativeBase,sessionmaker

class Base(DeclarativeBase):
    pass

engine = create_engine(url=app_settings.DB_CONNECTION)

LocalSession = sessionmaker(
    bind=engine
)

def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()