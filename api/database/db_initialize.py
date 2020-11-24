"""Main module for setting up database."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./api/database/local_sql.db"

ENGINE = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SESSIONLOCAL = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

Base = declarative_base()
