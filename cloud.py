# coding: utf-8

from django.core.wsgi import get_wsgi_application
from leancloud import Engine
from leancloud import LeanEngineError
import time
import random
import bisi_discuz

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
def bisi_reply_freevip():
    print('bisi_reply_freevip start...')
    time.sleep(random.randint(1,100))
    bisi_discuz.bisi_reply_mulit('免费VIP',random.randint(19,40))
    print('bisi_reply_freevip END!')
    
@engine.define
def bisi_reply_one():
#    print('start...')
#    time.sleep(random.randint(1,1000))
    print('bisi_reply_marx88 start...')
    time.sleep(random.randint(1,100))
    bisi_discuz.bisi_reply_mulit('marx88',random.randint(19,35))
    print('bisi_reply_marx88 END!')    