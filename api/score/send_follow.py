#coding=utf-8
import base64
import json
import time
import requests
import pymysql as mdb

#数据库操作，传入操作字符串，返回套着字典的列表
def query_sql(sql):
    #print(sql)
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

#发送消息
def send_qq(qq,msg):
    data={'user_id':qq,'message':msg+"\n\n〔学联宣传网络部〕"}
    print(data)
    requests.post("http://127.0.0.1:5700/send_msg/",data=data)
    with open("follow.log","a") as f: f.write(json.dumps(data,ensure_ascii=False)+"\n\n")

def update():
    with open("follow_ct.txt","r") as f: nowid=int(f.read())
    sql="select * from sports where id>{}".format(nowid)
    r=query_sql(sql)
    if len(r): print(time.strftime("%Y-%m-%d %H:%M:%S"))
    for i in r:
        sql="select * from follow where sid='{}'".format(i['sid'])
        rr=query_sql(sql)
        nowid=max(nowid,int(i['id']))
        for j in rr:
            msg="(°∀°)ﾉ您订阅的{}班{}同学的{}成绩更新啦~请访问 suours.com 查询".format(j['class'],j['name'],i['projects'])
            send_qq(j['qq'],msg)
    if len(r): print("NOW:",nowid)
    with open("follow_ct.txt","w") as f: f.write(str(nowid))

while True:
    update()
    time.sleep(60)