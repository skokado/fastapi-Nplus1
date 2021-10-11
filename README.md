参考: [Relationship Loading Techniques — SQLAlchemy 1.4 Documentation](https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html#relationship-loading-with-loader-options)

```shell
$ git clone fastapi-Nplus1
$ cd fastapi-Nplus1/
$ pipenv install
$ pipenv shell

$ # ダミーデータ作成
$ python3 gendata.py

$ # API起動
$ pipenv run dev

$ # 動作確認
$ curl localhost:8000/bad
$ curl localhost:8000/good
```

# クエリ確認

`joinedload`を使うことにより、テーブルを結合したクエリを実行する

実際に発行されるクエリの確認方法

```python
from sqlalchemy import dialects
from sqlalchemy.orm import joinedload

from app.dependencies import get_db
from app.models import Category, Blog

db = next(get_db())

# Bad
bad_query = db.query(Blog)
bad_dialect = bad_query.statement.compile(dialect=dialects.sqlite.dialect())
print(bad_dialect)
# => SELECT blogs.id, blogs.title, blogs.content, blogs.category_id 
#    FROM blogs


# Good
good_query = db.query(Blog).options(joinedload(Blog.category))
good_dialect = good_query.statement.compile(dialect=dialects.sqlite.dialect())
print(good_dialect)
# => SELECT blogs.id, blogs.title, blogs.content, blogs.category_id, categories_1.id AS id_1, categories_1.name 
#    FROM blogs LEFT OUTER JOIN categories AS categories_1 ON categories_1.id = blogs.category_id
```
