# 发送邮件
from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


# 用于生成随机字符串
def random_str(random_length=8):
    string = ''
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"
    length = len(chars) - 1
    r = Random()
    for i in range(random_length):
        string += chars[r.randint(0, length)]
    return string


# 用于发送邮件
def send_register_mail(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = 'MxOnline在线注册激活'
        email_body = "请点击下面的链接激活你的帐号： http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM, recipient_list=[email])
        if send_status:
            pass