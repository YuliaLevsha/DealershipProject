from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from Customer.tokens import account_activation_token
from Customer.utils import send_message_to_email
from DjangoProject.settings import MESSAGE_TEMPLATES


def form_message(request, user, template, action_type):
    """Формирование сообщения для отправки на почту"""
    activation_url = reverse_lazy(
        action_type,
        kwargs={
            "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    message = template + f"http://{get_current_site(request).domain}{activation_url}"
    return message


def send_activation_email(request, user, action_type):
    """Передача сообщения в функцию отправления.
    action_type - name для url, требующего подтверждения по почте.
    settings содержит MESSAGE_TEMPLATES, который содержит шаблоны
    (message и subject) для подтверждения почты/сброса пароля
    """
    message = form_message(
        request=request,
        template=MESSAGE_TEMPLATES[action_type]["message"],
        action_type=action_type,
        user=user,
    )
    send_message_to_email(
        subject=MESSAGE_TEMPLATES[action_type]["subject"],
        message=message,
        recipient=user.email,
    )
