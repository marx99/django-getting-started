# coding: utf-8

from django.core.wsgi import get_wsgi_application
from leancloud import Engine
from leancloud import LeanEngineError
import time
import random
import bisi_discuz
import requests
from bs4 import BeautifulSoup
#import send_mail

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
    bisi_discuz.bisi_reply_mulit('免费VIP',random.randint(19,30))
    print('bisi_reply_freevip END!')
    
@engine.define
def bisi_reply_marx88():
#    print('start...')
#    time.sleep(random.randint(1,1000))
    print('bisi_reply_marx88 start...')
    time.sleep(random.randint(1,100))
    bisi_discuz.bisi_reply_mulit('marx88',random.randint(19,30))
    print('bisi_reply_marx88 END!')    
    
@engine.define
def bisi_reply_Freevip123():
#    print('start...')
#    time.sleep(random.randint(1,1000))
    print('bisi_reply_Freevip@123 start...')
    time.sleep(random.randint(1,20))
    bisi_discuz.bisi_reply_mulit('Freevip@123',random.randint(19,30))
    print('bisi_reply_Freevip@123 END!')    

@engine.define
def bisi_reply_All():
    list1 = ['免费VIP','marx88','Freevip@123','marx99']
    for user in list1:
        print(user)
        try:
            bisi_discuz.bisi_reply_mulit(user,1)
        except:
            pass

@engine.define
def get_bisi_group():
    url1 = 'http://hkbbcc.net/group.php?gid=434'
    #第2页
    url2 = 'http://hkbbcc.net/group.php?gid=434&orderby=displayorder&page=2'
    url_all=[url1,url2]
    f = open('output/'+time.strftime('%Y%m%d') + '.html','a',encoding='utf-8')
    for url in url_all:
        html = requests.get(url)     
    #    print(html.text)
        soup = BeautifulSoup(html.text)
    #    print('%' * 50)
        for link in soup.find_all('tr',class_='fl_row'):
#            f.write(str(link))
#            print(link)
            if link:
                read_tr(link)
        time.sleep(1)
#    print('%' * 50)
    f.close()
    
def read_tr(link):
    group_title = link.find_all('a',limit=1)[0].get('title')
    ren_num =link.find_all(class_='i_z z')[0].find_all('strong')[0].text
    zhuti_num=link.find_all(class_='i_y z')[0].find_all('strong')[0].text
    print(group_title,ren_num,zhuti_num)    