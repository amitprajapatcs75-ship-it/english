from celery import shared_task
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import send_mail

@shared_task
def auth_mail_send(subject, html_message, user_email):
    plain_message = strip_tags(html_message)
    try:
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [user_email],
            html_message=html_message
        )
        return "mail sent successfully"
    except Exception as e:
        return f"error to send mail: \n {str(e)}"