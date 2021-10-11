import time

from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session

from app.database import Base, engine
from app.dependencies import get_db
from app.models import Blog

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get('/')
def index():
    return {'detail': 'It works'}


@app.get('/bad')
def bad(db: Session = Depends(get_db)):
    start = time.time()
    queryset = db.query(Blog).all()
    process_time_querying = round(time.time() - start, 2)

    start = time.time()
    for blog in queryset:
        # print(blog.id, blog.title,  blog.category)
        blog.category.name
    process_time_iteration = round((time.time() - start), 2)
    return {
        'msg': f'fetched {len(queryset)} records',
        'process_time_querying': process_time_querying,
        'process_time_iteration': process_time_iteration
    }


@app.get('/good')
def good(db: Session = Depends(get_db)):
    start = time.time()
    # Here!
    queryset = db.query(Blog).options(joinedload(Blog.category)).all()
    process_time_querying = round(time.time() - start, 2)

    start = time.time()
    for blog in queryset:
        # print(blog.id, blog.title,  blog.category)
        blog.category.name
    process_time_iteration = round((time.time() - start), 2)
    return {
        'msg': f'fetched {len(queryset)} records',
        'process_time_querying': process_time_querying,
        'process_time_iteration': process_time_iteration
    }
