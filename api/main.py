from flask_cors import CORS
from flask import Flask,request
import base64
import json
import mail
import music

app = Flask(__name__)
CORS(app,resources=r"/*")

@app.route("/")
def say_hello():
    return "hello SF-ND!"

#发送邮件 参数: to sub msg (type name)
@app.route('/send_mail/',methods=['GET','POST'])
def send_mail():
    try:
        args=request.values
        to=args['to'] #邮箱地址
        subject=args["sub"] #标题
        #正文 检测是否base64编码
        if 'type'in args and args['type']=='base64': message=base64.b64decode(args['msg']).decode()
        else: message=args["msg"]
        #发送名字
        if 'from_name' in args: from_name=args['from_name']
        else: from_name="SF网络部_Official"
        #接受名字 默认为邮箱名
        if 'to_name' in args: to_name=args['to_name']
        else: to_name=to
        mail.send_mail(to,subject,message,from_name,to_name)
        return {'stauts':'ok'}
    except:
        return {'status':'error'}

#点歌系统
@app.route('/music/',methods=['GET','POST'])
def music_():
    args=request.values
    return music.main(args['cmd'],json.loads(args['data']))


app.run(host="0.0.0.0",port=5705)
