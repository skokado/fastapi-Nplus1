import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, unique=True)
    blogs = relationship('Blog', back_populates='category')


class Blog(Base):
    __tablename__ = 'blogs'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String)
    content = sa.Column(sa.Text)
    category = relationship('Category', back_populates='blogs')
    category_id = sa.Column(sa.Integer, sa.ForeignKey('categories.id'))
