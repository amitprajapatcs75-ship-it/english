from django.template.loader import render_to_string
import random
from django.core.cache import cache
from users.task import auth_mail_send
from datetime import datetime

def send_otp_to_mail(username, user_email):
    otp =random.randint(100000, 999999)
    html_message = render_to_string('mail/otp_verification.html', {
        'fullname': username.title(),
        'otp':otp,
        "year": str(datetime.now().year)})
    cache.set(f"otp_{user_email}", otp, 60*10)
    subject = 'OTP for Verification'

    auth_mail_send.delay(subject, html_message, user_email)

def send_forget_password_otp(fullname, user_email, ):
    otp = random.randint(100000, 999999)
    html_message = render_to_string('mail/otp_verification.html',{
        'username': fullname.title(),
        'otp': otp,
        'year': str(datetime.now().year)
    })
    cache.set(f"forgot_otp_{user_email}", otp, 60*10)
    subject = 'Forget password email verification'
    auth_mail_send.delay(subject, html_message, user_email)