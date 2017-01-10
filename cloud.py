# coding: utf-8

from django.core.wsgi import get_wsgi_application
from leancloud import Engine
from leancloud import LeanEngineError
import sqlite3API

engine = Engine(get_wsgi_application())

@engine.define
def hello(**params):
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'


@engine.before_save('Todo')
def before_todo_save(todo):
    content = todo.get('content')
    if not content:
        raise LeanEngineError('内容不能为空')
    if len(content) >= 240:
        todo.set('content', content[:240] + ' ...')

@engine.define
def test_sqlite3():
    sql = 'select * from student order by RANDOM() limit 2'
    DB_FILE_PATH = 'hongten.db'
    conn = sqlite3API.get_conn(DB_FILE_PATH)
    sqlite3API.fetchall(conn,sql)