"""
@文件        :verifyPhone.py
@说明        :手机号验证服务 
@时间        :2024/01/16 15:17:51
@作者        :vagmr
@版本        :1.1
"""
import os
from twilio.rest import Client
from util.getEnv import init_env, get_env

init_env()

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
vasid = get_env('VASID')
client = Client(account_sid, auth_token)


def send_verify_code(phone):
    """
    发起对提供的电话号码进行短信验证。

    参数:
    phone (str): 将要发送验证代码的电话号码。

    返回:
    Verification对象: 包含已发送的验证代码的信息。
    """
    verification = client.verify.v2.services(vasid).verifications.create(to=f"+86{phone}", channel='sms')
    return verification


def verify_code(phone, code):
    """
    对提供的电话号码和验证码进行验证检查。

    参数:
    phone (str): 需要验证的电话号码。
    code (str): 发送到电话的验证码。

    返回:
    VerificationCheck对象: 包含验证检查的结果信息。
    """
    verification_check = client.verify.v2.services(vasid).verification_checks.create(to=phone, code=code)
    return verification_check
