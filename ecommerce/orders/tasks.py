from celery import shared_task

from . import mail


@shared_task
def send_mail(email):
    mail.order_notification(email)
