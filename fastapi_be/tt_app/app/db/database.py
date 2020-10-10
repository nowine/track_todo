from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

# Create a local Session class, differentiated from the Session class default provided by sqlalchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# Define the `Base` class of ORM
Base = declarative_base()

# from .models import User, Item, Project