from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DEFINE THE DATABASE CREDENTIALS
USER = "postgres"
PASSWORD = "123"
HOST = "127.0.0.1"
POST = 5432
DATABASE = "postgres"
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{POST}/{DATABASE}"

engine = create_engine(DATABASE_URL)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Initialize database
def init_db():
    Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    try:
        db = session()
        yield db
    finally:
        db.close()
