from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL
sync_engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(sync_engine)

def get_session():
    with Session(sync_engine) as session:
        yield session