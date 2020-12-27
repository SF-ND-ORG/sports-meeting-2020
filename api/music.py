#coding=utf-8
# 体育节2020点歌系统Python后端

import json
import time
import requests
import random
import pymysql as mdb

cold_time=15*60
pool_time=2*60*60

#数据库操作，传入操作字符串，返回套着字典的列表
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

#发送qq信息
def send_qq(qq,msg):
    data={'user_id':qq,'message':msg+"\n\n〔学联宣传网络部〕"}
    requests.post("http://127.0.0.1:5700/send_msg/",data=data)
    with open("send_qq.log","a") as f: f.write(json.dumps(data,ensure_ascii=False)+"\n\n")

#检查点歌冷却时间
def check_cold_time(qq):
    r=query_sql("select max(submit_time) as time from music where qq='{}'".format(qq))
    if r[0]['time'] and r[0]['time']>time.time()-cold_time: return False
    return True

#提交点歌
def submit(dic):
    data=dic['data']
    if check_cold_time(dic['qq']):
        sql="INSERT INTO music(mid,qq,data,status,submit_time)VALUES( \
            '{}','{}','{}',1,{})".format(data['mid'],dic['qq'], \
            mdb.escape_string(json.dumps(data,ensure_ascii=False)),int(time.time()))
        r=query_sql(sql)
        send_qq(dic['qq'],"小苏收到(･∀･)\n歌曲审核成功后将会通知您，欢迎访问 suours.com 探索更多~")
    else: send_qq(dic['qq'],"( ´_ゝ｀)\n15分钟内只能点一首歌呢....")

#查询点歌
def query(dic):
    try:
        if dic['type']=='split':
            sql="select * from music order by id desc limit {} offset {}".format(dic['limit'],dic['offset'])
            r=query_sql(sql)
            return {'status':'ok','data':r,'len':len(r)}
        
        if dic['type']=='merge_time':
            sql="select * from music where status=4 order by play_time desc limit {} offset {}".format(dic['limit'],dic['offset'])
            r=query_sql(sql)
            return {'status':'ok','data':r,'len':len(r)}
            
        if dic['type']=='merge_num':
            sql="select mid,count(*) as ct,max(data) as data from music group by mid order by ct desc,max(id) desc limit {} offset {}".format(dic['limit'],dic['offset'])
            r=query_sql(sql)
            return {'status':'ok','data':r,'len':len(r)}

        if dic['type']=='statis':
            sql="select count(status=1 or null) as waiting,count(judge_time>={} and status=2 or null) as pool,count(*) as total from music;".format(int(time.time()-pool_time))
            r=query_sql(sql)
            return {'status':'ok','data':r[0]}
        
        return {'status':'error'}
    except:
        return {'status':'error'}


#审核点歌
def judge(dic):
    try:
        sql="update music set status={},judge_time={} where id={}".format(dic['status'],int(time.time()),dic['id'])
        r=query_sql(sql)
        
        if dic['status']==2: send_qq(dic['qq'],"您的歌曲[{}]审核通过啦~\n_(:з」∠)_将在接下来两个小时内随机播放。访问 suours.com/music 查看点歌榜单及播放列表，祝您体育节玩得开心！".format(dic['name']))
        if dic['status']==3: send_qq(dic['qq'],"emm您的歌曲[{}]审核未通过呢....\n(´；ω；`)换一首试试嘛~访问 suours.com/music 查看点歌榜单及播放列表，祝您体育节玩得开心！".format(dic['name']))

        return {'status':'ok','data':r,'len':len(r)}
    except:
        return {'status':'error'}

#获取播放音乐
def play(dic):
    #try:
    if True:
        sql="select * from music where status=5 order by judge_time desc"
        r=query_sql(sql)
        if len(r): m=r[0]
        else:
            sql="select * from music where status=2 and judge_time>={}".format(int(time.time()-pool_time))
            r=query_sql(sql)
            if len(r)==0: return {'status':'empty'}
            m=r[random.randint(0,len(r)-1)]

        sql="update music set status=4,play_time={} where id={}".format(int(time.time()),m['id'])
        query_sql(sql)
        return {'status':'ok','data':m}
    #except:
    #    return {'status':'error'}
    


def main(cmd,data):
    if cmd=='submit': submit(data)
    if cmd=='judge': return judge(data)
    if cmd=='query': return query(data)
    if cmd=='play': return play(data)

    return {"status":"ok"}

#submit({'qq':'1525876733','data':{'mid':'S0','name':'2333'}})
