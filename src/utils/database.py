from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DEFINE THE DATABASE CREDENTIALS
user = "postgres"
password = "123"
host = "127.0.0.1"
port = 5432
database = "postgres"
DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

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
