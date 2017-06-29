# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 10:18:20 2016

@author: Administrator
"""

import requests
#import urllib.request
import re
#from mysqlAPI import mysqlAPI
from discuzAPI import DiscuzAPI
import random
import time
import sqlite3API

DB_FILE_PATH = 'hongten.db'

def bisi_reply_mulit(userid = 'marx88' , total=100):
    
#    mysql = mysqlAPI('test')
#    info_tid = mysql.select_mysql('select id from bisi_discuz where reply_num > 40 order by RAND() limit ' + str(total))
#    info_content = mysql.select_mysql('select content from reply_content order by RAND() limit ' + str(total*3))
#    mysql.close_mysql()

    sql_tid ='select id,title from bisi_discuz where reply_num > 10 order by RANDOM() limit ' + str(total)
    sql_content = 'select content from reply_content order by RANDOM() limit ' + str(total*3)
    
    conn = sqlite3API.get_conn(DB_FILE_PATH)
    info_tid=sqlite3API.fetchmany(conn,sql_tid)
    info_content=sqlite3API.fetchmany(conn,sql_content)
    data=userid
    info_user = sqlite3API.fetchone(conn,"select url,user,password from master where user=?",data)
    url = info_user[0]
    user=info_user[1]
    password=info_user[2]
#    print (password)
    discuz = DiscuzAPI(url,user,password)       
    discuz.login()
    discuz.sign()
    
    total = len(info_content)
    
    for tid in info_tid:
#        print(info_content[random.randint(0,total-1)][0])
        msg = info_content[random.randint(0,total-1)][0]
        try:
            discuz.reply(tid[0],msg='%s,%s' % (tid[1],msg))
        except:
            pass
        time.sleep(random.randint(65,70))

def getListBisi(url):
    try:
        html = requests.get(url,timeout=5)
    
    #    rege1 = re.compile( '>([^<]+)</a>\]</em> <a href="thread-([0-9]+)-1-[0-9]+.html"[^>]+>([^<]+)</a>\n[^\n]+\n[^\n]+\n[^\n]+\n[^\n]+\n[^\n]+\n<a href="([^"]+)"[^>]+>([^<]+)</a>[^\n]+\n<em><span>([^<]+)</span></em>\n</td>\n<td class="num"><a [^>]+>([0-9]+)</a><em>([0-9]+)</em></td>')
        regex = re.compile( '>([^<]+)</a>\]</em> <a href="thread-([0-9]+)-1-[0-9]+.html"[^>]+>([^<]+)</a>[^\n]*\n[^\n]+\n[^\n]+\n[^\n]+\n[^\n]+\n[^\n]+\n<a href="([^"]+)"[^>]+>([^<]+)</a>[^\n]+\n<em><span>([^<]+)</span></em>[^\n]*\n[^\n]*\n<td class="num"><a [^>]+>([0-9]+)</a><em>([0-9]+)</em></td>')
        rows = regex.findall(html.text)
        print((rows))
        
        print('regex',len(rows))
    #    return
        
        conn = sqlite3API.get_conn(DB_FILE_PATH)
        save_sql ='insert ignore into bisi_discuz_test values(?,?,?,?,?,?,?,?,now())'
        sqlite3API.save(conn, save_sql, rows)
#        mysql = mysqlAPI('test')
#        mysql.insert_mysql('insert ignore into bisi_discuz_test values(%s,%s,%s,%s,%s,%s,%s,%s,now())',rows)
#        mysql.close_mysql()
    except:
        pass
    
    time.sleep(1)

def getReplyContent(url):
    
    try:
        html = requests.get(url,timeout=5)
        regex = re.compile('<td class="t_f"[^\n]+\n([^<]+)<')
        rows = regex.findall(html.text)
#        print(rows)
        conn = sqlite3API.get_conn(DB_FILE_PATH)
        save_sql ="insert ignore into reply_content (content,flg) values(?,'0')"
        sqlite3API.save(conn, save_sql, rows)
    
#        mysql = mysqlAPI('test')
#        mysql.insert_mysql("insert ignore into reply_content (content,flg) values(%s,'0')",rows)
#        mysql.close_mysql()
    except:
        pass
    time.sleep(1)
    
if __name__ == '__main__':
    bisi_reply_mulit('marx99',random.randint(1,2))