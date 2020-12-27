# -*- coding: utf-8 -*-
import requests
import json
import re
import pymysql as mdb

def query_sql(sql):
    con=mdb.connect('localhost','root','','ours',charset='utf8')
    cur=con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    des=cur.description
    l=[]
    for row in cur.fetchall():
        dis={}
        for i in range(len(cur.description)):
            dis[cur.description[i][0]]=row[i]
        l.append(dis)
    return l

def bili_music(mid):
    r=requests.get("http://127.0.0.1:5000/bilimusic/?type=music&mid="+mid)
    #print("http://127.0.0.1:5000/bilimusic/?type=music&mid=B"+vid)
    info=json.loads(r.text)
    return info

def cloud_music(mid):
    r=requests.get("https://1426531544223608.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/music/cloudmusic/?type=music&mid="+mid)
    info=json.loads(r.text)
    return info

def qq_music(mid):
    r=requests.get("https://1426531544223608.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/music/qqmusic/?type=music&mid="+mid)
    info=json.loads(r.text)
    return info

def get_music_data(mid):
    if mid[0]=="B": info=bili_music(mid)
    if mid[0]=="C": info=cloud_music(mid)
    if mid[0]=="Q": info=qq_music(mid)

    print(info['name'])

    info.pop("lrc")
    info.pop("src")
    info.pop("img")
    data=json.dumps(info,ensure_ascii=False)
    return data

sql="select * from music"
r=query_sql(sql)
for i in r:
    data=get_music_data(i["mid"])
    sql="update music set data='{}' where id={}".format(data,i['id'])
    query_sql(sql)