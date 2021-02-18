import requests
import json
import urllib3
import os
import hashlib
import datetime
import smtplib
from email.mime.text import MIMEText

urllib3.disable_warnings()

# username = os.environ['USERNAME']
# password = os.environ['PASSWORD']
# mail     = os.environ['MAIL']
# success  = os.environ['SUCCESS']
# key      = os.environ['KEY']
username = 'haycvbnm@163.com'
password = '123456789zy'
success = 'SCU156152T14435ae80a60fcecdae6da9d67842bca60138c301ed8d'
mail = 'bokezy@qq.com'
key = 'fumqpbhroyvhdhge'


# 获取北京时间函数
def GetNowTime():
    cstTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    strTime = cstTime.strftime("%H:%M:%S")
    return strTime


def Sign(username, password):
    login_url = 'https://note.youdao.com/login/acc/urs/verify/check?app=web&product=YNOTE&tp=urstoken&cf=6&fr=1&systemName=&deviceType=&ru=https%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2FloginCallback.html&er=https%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2FloginCallback.html&vcode=&systemName=mac&deviceType=MacPC&timestamp=1611466345699'
    checkin_url = 'http://note.youdao.com/yws/mapi/user?method=checkin'

    parame = {
        'username': username,
        'password': hashlib.md5(password.encode('utf8')).hexdigest(),
    }
    s = requests.Session()
    try:
        # 登录
        s.post(url=login_url, data=parame, verify=False)
        # 签到
        r = s.post(url=checkin_url)
    except:
        print('没连上网' + '\n' + '有道云签到失败')
        WechatPush('有道云签到失败', success, username, '0', '没连上网')
        sendEmail(mail, key, '有道云签到失败', '没连上网')
        exit()
    print(r.text)
    if r.status_code == 200:
        info = json.loads(r.text)
        total = info['total'] / 1048576
        space = info['space'] / 1048576
        t = GetNowTime()
        print('{} | 这次签到获得：{} M | 总共获得：{} M | 签到时间：{}'.format(username, space, total, t))
        WechatPush('有道云签到成功', success, username, space, '总共获得'+str(total)+ 'M')
        sendEmail(mail, key, '有道云签到成功', username+'有道云签到成功' + '\n' + '这次签到获得：' + str(space) + 'M' '\n' + '总共获得'+str(total)+ 'M')
    else:
        WechatPush('有道云签到失败', success, username, '0', r.text)
        sendEmail(mail, key, '有道云签到失败', r.text)
        exit()


def WechatPush(title, sckey, username, fail, total):
    send_url = f"http://sc.ftqq.com/{sckey}.send"
    strTime = GetNowTime()
    page = json.dumps(total, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
    content = [f"""`{strTime}`
#### 账号:
`{username}`
#### 这次签到获得：:
`{fail}M`
#### 信息:
```
{page}
```"""]
    data = {
        "text": title,
        "desp": content
    }
    try:
        req = requests.post(send_url, data=data)
        if req.json()["errmsg"] == 'success':
            print("Server酱推送服务成功")
        else:
            print("Server酱推送服务失败")
    except:
        print("Server酱推送异常")


def sendEmail(mail, key, subject, txt):
    msg_from = 'bokezy@qq.com'  # 发送方邮箱，
    passwd = ''.join(key)
    msg_to = ''.join(mail)
    content = GetNowTime() + '\n' + txt
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        send = smtplib.SMTP_SSL("smtp.qq.com", 465)
        send.login(msg_from, passwd)
        send.sendmail(msg_from, msg_to, msg.as_string())
        print(mail + '  ' + "邮箱推送成功")
    except Exception:
        print(mail + '  ' + "邮箱推送失败")


if __name__ == "__main__":
    Sign(username, password)
    # WechatPush('有道云签到失败', success, username, '1', '1')
    # sendEmail('bokezy@qq.com', 'fumqpbhroyvhdhge', '有道云_签到成功', '有道云_签到成功')
