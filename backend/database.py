# SQLAlchemy engine and session setup
from sqlmodel import create_engine, SQLModel

DATABASE_URL = "sqlite:///./phonebook.db"

# connect_args zostaje bez zmian dla SQLite
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    echo=True
)

# Function to initialize tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)