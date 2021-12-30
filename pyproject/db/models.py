from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from .modelbase import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    view_count = Column(Integer, nullable=False, default=0)
    title = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    markdown = Column(Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.id}: {self.title}, '{self.created_at}')"
