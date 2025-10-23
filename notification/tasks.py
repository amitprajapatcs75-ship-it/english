from celery import shared_task
from notification.push_notification import send_push_notification

@shared_task
def send_notification_task(title,body, token):
    try:
        send_push_notification(title=title, body=body, token=token)
        print("notification send")
    except Exception as e:
        print(f"notification send error in celery task {e}")