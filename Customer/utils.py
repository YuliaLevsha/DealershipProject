import os

from django.core.mail import send_mail


def send_message_to_email(subject: str, message: str, recipient: str) -> None:
    """Отправка полученного сообщения на переданную почту"""
    send_mail(subject=subject,
              message=message,
              from_email=os.environ.get("EMAIL_HOST_USER"),
              recipient_list=[recipient],
              fail_silently=False
              )
