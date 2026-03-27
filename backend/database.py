# SQLAlchemy engine and session setup
from sqlmodel import create_engine, SQLModel

DATABASE_URL = "sqlite:///./phonebook.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    echo=True
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)