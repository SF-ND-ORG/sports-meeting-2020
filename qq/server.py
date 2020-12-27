# -*- coding: utf-8 -*-
from flask import Flask,request
import requests
import json
import re

import follow

app=Flask(__name__)

def send_qq(qq,msg):
    data={'user_id':qq,'message':msg+"\n\n〔学联宣传网络部〕"}
    requests.post("http://127.0.0.1:5700/send_msg/",data=data)

def bili_music(s):
    global flag
    share_url=re.search("https://b23.tv/[A-z0-9]+",s).group()
    flag="B"
    r=requests.get(share_url,allow_redirects=False)
    vid=re.search("BV\S+?p=[0-9]+",r.text).group()
    r=requests.get("http://127.0.0.1:5000/bilimusic/?type=music&mid=B"+vid)
    #print("http://127.0.0.1:5000/bilimusic/?type=music&mid=B"+vid)
    info=json.loads(r.text)
    return info

def cloud_music(s):
    global flag
    try: share_url=re.search("https://y.music.163.com/m/song[?]id=[0-9]+",s).group()
    except: share_url=re.search("https://y.music.163.com/m/song/[0-9]+",s).group()
    flag="C"
    mid="C"+re.findall("[0-9]+",share_url)[-1]
    r=requests.get("https://1426531544223608.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/music/cloudmusic/?type=music&mid="+mid)
    info=json.loads(r.text)
    return info

def qq_music(s):
    global flag
    try:
        ori_url=re.search("https://c.y.qq.com/base/fcgi-bin/u\?__=[A-z0-9]+",s).group()
        r=requests.get(ori_url)
        share_url=re.search("mid=[A-z0-9]+",r.text.replace("&#61;","=")).group()
    except:
        try: share_url=re.search("songmid=[A-z0-9]+",s).group()
        except: share_url=re.search("media_mid=[A-z0-9]+",s).group()
    flag="Q" 
    mid="Q"+re.search("=[A-z0-9]+",share_url).group()[1:]
    r=requests.get("https://1426531544223608.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/music/qqmusic/?type=music&mid="+mid)
    info=json.loads(r.text)
    return info

def music_share(dic):
    global flag
    if dic['ClassType']!='PrivateMessage': return
    info=None
    flag=None
    
    s=json.dumps(dic,ensure_ascii=False).replace('\\','')
    try: info=bili_music(s)
    except: pass
    try: info=cloud_music(s)
    except: pass
    try: info=qq_music(s)
    except: pass
    
    if not flag: return
    if not info or info['src']=='':
        send_qq(dic['user_id'],'(;¬_¬)好像哪里不大对劲诶....\n可尝试更换歌曲或平台(bilibili|网易云|QQ)')
        return

    msg='[CQ:music,type=custom,url={},audio={},title={},image={},content={}]'.format(
        "http://suours.com/music/#/?mid="+info['mid'],
        info['src'],
        info['name'],
        info['img'],
        "Ours-MergeMusic"
    )

    print(info['name'])
    send_qq(dic['user_id'],msg)

    info.pop("lrc")
    info.pop("src")
    info.pop("img")
    if "tlrc" in info:info.pop("tlrc")
    data={"cmd":"submit","data":json.dumps({"qq":str(dic['user_id']),"data":info},ensure_ascii=False)}
    r=requests.post("http://127.0.0.1:5705/music/",data=data)

@app.route('/',methods=['POST'])
def main():
    dic=json.loads(request.data.decode('utf-8'))
    print(dic)

    if dic['post_type']=='meta_event': return ''
    
    try: music_share(dic)
    except: pass
    #music_share(dic)

    try: follow.follow(dic)
    except: pass
    
    if dic['ClassType']=='PrivateMessage':
        with open("./log.txt","a") as f:
            f.write(json.dumps(dic)+"\n\n")

    return {'status':'ok'}

app.run(host='0.0.0.0',port=5701)
