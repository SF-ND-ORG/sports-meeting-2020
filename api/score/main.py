#coding=utf-8
from flask_cors import CORS
from flask import Flask,request
import base64
import json
import time
import pymysql as mdb

app = Flask(__name__)
CORS(app,resources=r"/*")

@app.route("/")
def say_hello():
    return "hello SF-ND!"

#数据库操作，传入操作字符串，返回套着字典的列表
def query_sql(sql):
    print(sql)
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

#查询学号
def get_sid(cla,name):
    sql="select sid from students where class='{}' and name='{}'".format(cla,name)
    r=query_sql(sql)
    return r[0]['sid']

#是否已经加入过
def check(gra,cla,name,pro):
    sql="select * from sports where grades='{}' and class='{}' and name='{}' and projects='{}'".format(gra,cla,name,pro)
    r=query_sql(sql)
    if len(r):return False
    return True

#按年级+班级查成绩
@app.route('/getgrades/byclass/',methods=['GET','POST'])
def class_grades():
    args="SELECT * FROM sports where grades='"+request.values.get('grades')+"' and class='"+request.values.get('class')+"'"
    myresult = query_sql(args)

    return {"data":myresult}

#按年级+班级+名字查成绩
@app.route('/getgrades/byname/',methods=['GET','POST'])
def name_grades():
    args="SELECT * FROM sports where grades='"+request.values.get('grades')+"' and class='"+request.values.get('class')+"' and name='"+request.values.get('name')+"'"
    myresult = query_sql(args)

    return {"data":myresult}

#按项目查成绩
@app.route('/getgrades/bypro/',methods=['GET','POST'])
def pro_grades():
    args="SELECT * FROM sports where projects='"+request.values.get('projects')+"'"
    myresult = query_sql(args)

    return {"data":myresult}

#查询当前项目
@app.route('/projects/',methods=['GET','POST'])
def projects():
    args="select projects from sports group by projects"
    myresult = query_sql(args)
    l=[i['projects'] for i in myresult]

    return {"data":l,"len":len(l)}

#上传成绩
@app.route("/upgrades/",methods=['GET','POST'])
def up_date():
    data=request.values.get('data')
    dic=json.loads(data)
    print(dic)
    for i in dic:
        try:
            if i['name']=="团体": i['sid']=""
            else: i['sid']=get_sid(i['grades']+i['class'],i['name'])
        except: return "error with {} {}".format(i['grades']+i['class'],i['name'])
        if check(i['grades'],i['class'],i['name'],i['projects'])==False: return "repeat {}".format(i['name'])
    for i in dic:
        sql = "INSERT INTO sports (grades, class, name, achievements,projects,rank,sid,time) VALUES ('%s', '%s', '%s', '%s' ,'%s', '%s','%s',%d)" % \
            (str(i['grades']), str(i["class"]), str(i["name"]),\
            str(i["achievements"]),str(i["projects"]),str(i["rank"]),str(i["sid"]),int(time.time()))
        query_sql(sql)
    return "update successfully"

#添加订阅
@app.route('/follow/up/',methods=['GET','POST'])
def follow_up():
    try:
        dic=request.values.to_dict()
        try: sid=get_sid(dic['class'],dic['name'])
        except: return {"status":"empty"}
        sql="select * from follow where qq='{}' and sid='{}'".format(dic['qq'],sid)
        r=query_sql(sql)
        if len(r):
            print(type(r[0]['status']))
            if r[0]['status']==1: return {"status":"repeat"}
            sql="update follow set status=1 where id={}".format(r[0]['id'])
            query_sql(sql)
        else:
            sql="insert into follow (sid,class,name,qq,time,status) values \
                ('{}','{}','{}','{}',{},1)".format(sid,dic['class'],dic['name'],dic['qq'],int(time.time()))
            query_sql(sql)
        return {"status":"ok"}
    except: return {"status":"error"}

#订阅列表
@app.route('/follow/list/',methods=['GET','POST'])
def follow_list():
    try:
        dic=request.values.to_dict()
        sql="select * from follow where status=1 and qq='{}'".format(dic['qq'])
        r=query_sql(sql)
        return {"status":"ok","data":r}
    except: return {"status":"error"}

#取消订阅
@app.route('/follow/delete/',methods=['GET','POST'])
def follow_delete():
    try:
        dic=request.values.to_dict()
        sql="update follow set status=0 where qq='{}' and id={}".format(dic['qq'],dic['id'])
        query_sql(sql)
        return {"status":"ok"}
    except: return {"status":"error"}

app.run(host="0.0.0.0",port=5706)
