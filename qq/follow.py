# -*- coding: utf-8 -*-
import requests
import json
import re
import html


#发送消息
def send_qq(qq,msg):
    data={'user_id':qq,'message':msg+"\n\n〔学联宣传网络部〕"}
    requests.post("http://127.0.0.1:5700/send_msg/",data=data)
    with open("send_qq.log","a") as f: f.write(json.dumps(data,ensure_ascii=False)+"\n\n")

#订阅选手
def follow(dic):
    if dic['ClassType']!='PrivateMessage': return
    qq=dic['user_id']
    msg=html.unescape(dic['raw_message']).split()
    print(msg)
    try:
        if msg[0]=="#订阅选手":
            data={"qq":qq,"class":msg[1],"name":msg[2]}
            r=requests.get("http://127.0.0.1:5706/follow/up/",data=data)
            dic=json.loads(r.text)
            if dic['status']=="error": 0/0
            if dic['status']=="empty": send_qq(qq,"这位同学好像不存在的亚子....\n班级示例：231|22L1|21W1")
            if dic['status']=="repeat": send_qq(qq,"已经订阅过啦~\n回复“#订阅列表”可查看当前订阅的选手")
            if dic['status']=="ok": send_qq(qq,"订阅成功啦(･∀･)\n选手成绩更新后小苏将会通知您！回复“#订阅列表”可查看当前订阅选手，欢迎访问 suours.com 探索更多~\n祝您体育节玩得开心！")
        if msg[0]=="#订阅列表":
            data={"qq":qq}
            r=requests.get("http://127.0.0.1:5706/follow/list/",data=data)
            dic=json.loads(r.text)
            if dic['status']=="error": 0/0
            l=dic['data']
            reply="ID | 班级 | 姓名\n"
            for i in l: reply+="{} | {} | {}\n".format(i['id'],i['class'],i['name'])
            reply+="共订阅{}位选手\n".format(len(l))
            reply+="回复“#取消订阅  ID”可取消订阅"
            send_qq(qq,reply)
        if msg[0]=="#取消订阅":
            data={"qq":qq,"id":msg[1]}
            r=requests.get("http://127.0.0.1:5706/follow/delete/",data=data)
            dic=json.loads(r.text)
            if dic['status']=="error": 0/0
            if dic['status']=="ok": send_qq(qq,"取消成功(･∀･)\n欢迎访问 suours.com 探索更多~")
        if msg[0]=="订阅选手":
            send_qq(qq,"回复“#订阅选手  班级  姓名”即可订阅选手，选手成绩更新后将会通知您~（班级示例：231|22L1|21W1）\n回复“#订阅列表”可查看当前订阅的选手，也可根据提示取消订阅。")
        if msg[0]=="体育节":
            send_qq(qq,"欢迎访问 suours.com 探索更多~\n点歌请直接分享歌曲给小苏（也就是我啦），支持bilibili|网易云|QQ音乐（甚至权贵歌也是可以的！）\n成绩查询请访问网站，也可回复“订阅选手”以获取订阅服务\n有其他问题可直接发送，小苏将及时解答（大概，如果小苏没有在摸鱼的话）\n祝您体育节玩得开心！\n(*°▽°*)八(*°▽°*)♪")
        if msg[0][:2]=="谢谢":
            send_qq(qq,"不客气_(:з」∠)_")
        if msg[0]=="点歌":
            send_qq(qq,"点歌请直接分享歌曲给小苏（也就是我啦），支持bilibili|网易云|QQ音乐（甚至权贵歌也是可以的！）\n欢迎访问 suours.com 探索更多~")
    except: send_qq(qq,"qwq好像哪里不大对劲的亚子....可访问 suours.com 查看帮助")

