from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.test import APIClient
from Customer.models import Customer
from Customer.views import *
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from Customer.tokens import account_activation_token


USER_NAME = "Dream27"
EMAIL = "test@mail.ru"
PASSWORD = "testpassword"


class RegisterTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.view = RegisterViewSet.as_view({"post": "create"})

    def test_create(self):
        request = self.factory.post(
            "api/register/",
            data={
                "username": USER_NAME,
                "email": EMAIL,
                "password": PASSWORD,
                "password2": PASSWORD,
            },
        )
        response = self.view(request)
        self.assertEquals(response.status_code, 201)


class LoginTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.view = LoginView.as_view()
        self.user = Customer.objects.create_user(
            username=USER_NAME, email=EMAIL, password=PASSWORD
        )

    def test_post(self):
        request = self.factory.post(
            "api/login/", data={"username": USER_NAME, "password": PASSWORD}
        )
        response = self.view(request)
        self.assertEquals(response.status_code, 200)


class LogoutTest(TestCase):
    def setUp(self) -> None:
        self.user = Customer.objects.create_user(
            username=USER_NAME, email=EMAIL, password=PASSWORD
        )
        self.client = APIClient()
        self.refresh_token = self.user.tokens()["refresh"]
        self.access_token = self.user.tokens()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_post(self):
        response = self.client.post(
            "/api/logout/",
            data={
                "refresh_token": self.refresh_token,
            },
        )
        self.assertEquals(response.status_code, 205)


class ForgotPasswordTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.view = ForgotPasswordView.as_view()
        self.user = Customer.objects.create_user(
            username=USER_NAME, email=EMAIL, password=PASSWORD
        )

    def test_post(self):
        request = self.factory.post("api/forgot-password/", data={"email": EMAIL})
        response = self.view(request)
        self.assertEquals(response.status_code, 200)


class ChangePasswordTest(TestCase):
    def setUp(self) -> None:
        self.user = Customer.objects.create_user(
            username=USER_NAME, email=EMAIL, password=PASSWORD
        )
        self.client = APIClient()
        self.token = self.user.tokens()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_update(self):
        response = self.client.put(
            "/api/change-password/",
            data={
                "old_password": PASSWORD,
                "new_password": "whitesnake",
                "confirmation_password": "whitesnake",
            },
        )
        self.assertEquals(response.status_code, 200)


class UpdateUsernameEmailTest(TestCase):
    def setUp(self) -> None:
        self.user = Customer.objects.create_user(
            username=USER_NAME, email=EMAIL, password=PASSWORD
        )
        self.client = APIClient()
        self.token = self.user.tokens()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_update(self):
        response = self.client.put(
            "/api/update-user/", data={"username": "YuliaL", "email": EMAIL}
        )
        self.assertEquals(response.status_code, 200)


class ConfirmEmailTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = Customer.objects.create(
            username=USER_NAME,
            email=EMAIL,
            password=make_password(PASSWORD),
            is_active=False,
        )
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)

    def test_retrieve(self):
        url = reverse(
            "confirm_email", kwargs={"uidb64": self.uidb64, "token": self.token}
        )
        response = self.client.get(url)
        result_excpect = JsonResponse({"Email was confirmed": "Yes!"}).content
        self.assertEquals(response.content, result_excpect)


class ResetPasswordTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = Customer.objects.create_user(
            username=USER_NAME, email=EMAIL, password=PASSWORD
        )
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)

    def test_retrieve(self):
        url = reverse(
            "reset_password", kwargs={"uidb64": self.uidb64, "token": self.token}
        )
        response = self.client.put(
            url,
            data={"new_password": "whitesnake", "confirmation_password": "whitesnake"},
        )
        self.assertEquals(response.status_code, 200)
