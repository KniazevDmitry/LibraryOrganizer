from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///.test.db"

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    description = Column(String)


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
