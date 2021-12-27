import os
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.getenv("DATABASE_URI", "sqlite:///posts.db"), echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.id}: {self.title}, '{self.date_posted}')"
