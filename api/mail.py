#coding=utf-8

import smtplib
from email.utils import formataddr
from email.mime.text import MIMEText

# to为接收地址 subject为邮件标题 message为正文内容
def send_mail(to,subject,message,from_name="SF网络部_Official",to_name="NULL"):
    msg=MIMEText(message,"html","utf-8") #邮件内容
    msg['Subject']=subject #邮件标题
    msg['From']=formataddr([from_name,"3253541727@qq.com"]) #发送者
    msg['To']=formataddr([to_name,to]) #接收者
    SMTP=smtplib.SMTP_SSL("smtp.qq.com")
    SMTP.login("3253541727@qq.com","")
    SMTP.sendmail("3253541727@qq.com",to,msg.as_string())
    SMTP.quit()

#send_mail("1525876733@qq.com","测试","<h1>2333</h1>")

