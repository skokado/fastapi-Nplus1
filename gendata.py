import sys
import random

from faker import Faker
from sqlalchemy.orm.session import Session
from tqdm import tqdm

from app.models import Category, Blog
from app.database import Base, engine
from app.dependencies import get_db

Base.metadata.create_all(bind=engine)
faker = Faker()
DEFAULT_POSTS_RECORDS = 100000

CATEGORY_CHOICES = (
    'プログラミング',
    'デザイン',
    'マネジメント',
    'ビジネス',
    'その他',
)


def main(n: int, db: Session):
    categories = []
    for category in CATEGORY_CHOICES:
        categories.append(Category(
            name=category
        ))
    try:
        db.bulk_save_objects(categories, update_changed_only=True)
        db.commit()
    except:
        db.rollback()

    posts = [
        Blog(
            title=faker.text(),
            content=' '.join(faker.texts()),
            category_id=random.choice(range(1, len(CATEGORY_CHOICES) + 1))
        )
        for _ in tqdm(range(n))
    ]
    db.bulk_save_objects(posts)
    db.commit()
    print(f'Generated {n} post records')


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        n = DEFAULT_POSTS_RECORDS
    else:
        n = int(args[1])
    db = next(get_db())
    main(n, db)
