from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://pi:Nil0911@192.168.31.193:5432/track_todo"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a local Session class, differentiated from the Session class default provided by sqlalchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# Define the `Base` class of ORM
Base = declarative_base()

# from .models import User, Item, Project