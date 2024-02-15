from django.contrib.sites.shortcuts import get_current_site
import os
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail


def send_to_email(request, subject, user, name_url, message):
    current_site = get_current_site(request)
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = current_site.domain
    activation_url = reverse_lazy(name_url, kwargs={"uidb64": uid, "token": token})
    send_mail(
        subject=subject,
        message=message + f"{domain}{activation_url}",
        from_email=os.environ.get("EMAIL_HOST_USER"),
        recipient_list=[user.email],
        fail_silently=False,
    )