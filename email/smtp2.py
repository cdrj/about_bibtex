import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os,re



from_addr="836335723@qq.com"    #邮件发送账号
to_addrs='jsszdrj@163.com'   #接收邮件账号
qqCode='ksiuzolgzwadbcad'   #授权码（这个要填自己获取到的）
smtp_server='smtp.qq.com'#固定写死
smtp_port=465#固定端口



#配置服务器
stmp=smtplib.SMTP_SSL(smtp_server,smtp_port)
stmp.login(from_addr,qqCode)

#组装发送内容
message = MIMEText('local_ip', 'plain', 'utf-8')   #发送的内容
message['From'] = Header("Python邮件预警系统", 'utf-8')   #发件人
message['To'] = Header("管理员", 'utf-8')   #收件人
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')  #邮件标题

try:
    stmp.sendmail(from_addr, to_addrs, message.as_string())
except Exception as e:
    print ('邮件发送失败--' + str(e))
print ('邮件发送成功')
