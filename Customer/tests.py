from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from Customer.models import Customer
from Customer.views import *
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from Customer.tokens import account_activation_token


USER_NAME = "Dream27"
EMAIL = "test@mail.ru"
PASSWORD = "testpassword"


class AuthTest(TestCase):
    def setUp(self) -> None:
        self.user = Customer.objects.create_user(
            username=USER_NAME, email=EMAIL, password=PASSWORD
        )
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)
        self.client = APIClient()
        self.refresh_token = self.user.tokens()["refresh"]
        self.access_token = self.user.tokens()["access"]

    def test_register(self) -> None:
        bad_response = self.client.post(
            "/api/register/",
            data={
                "username": USER_NAME,
                "email": EMAIL,
                "password": PASSWORD,
                "password2": PASSWORD,
            },
        )
        correct_response = self.client.post(
            "/api/register/",
            data={
                "username": "testusername",
                "email": "help@mail.ru",
                "password": PASSWORD,
                "password2": PASSWORD,
            },
        )
        self.assertEquals(correct_response.status_code, 201)
        self.assertEquals(bad_response.status_code, 400)

    def test_login(self) -> None:
        bad_response = self.client.post(
            "/api/login/", data={"username": USER_NAME, "password": "fakepassword"}
        )
        correct_response = self.client.post(
            "/api/login/",
            data={
                "username": USER_NAME,
                "password": PASSWORD,
            },
        )
        self.assertEquals(correct_response.status_code, 200)
        self.assertEquals(bad_response.status_code, 401)

    def test_logout(self) -> None:
        bad_response = self.client.post(
            "/api/logout/",
            data={"refresh_token": ""},
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        correct_response = self.client.post(
            "/api/logout/",
            data={"refresh_token": self.refresh_token},
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(correct_response.status_code, 204)
        self.assertEquals(bad_response.status_code, 400)

    def test_confirm_email(self) -> None:
        correct_url = reverse(
            "confirm_email", kwargs={"uidb64": self.uidb64, "token": self.token}
        )
        correct_response = self.client.get(correct_url)
        test_user = Customer.objects.create_user(
            username="Badtest", email="help@mail.ru", password="whitesnake"
        )
        bad_url = reverse(
            "confirm_email",
            kwargs={
                "uidb64": self.uidb64,
                "token": account_activation_token.make_token(test_user),
            },
        )
        bad_response = self.client.get(bad_url)
        self.assertEquals(correct_response.status_code, 200)
        self.assertEquals(bad_response.status_code, 404)


class UserTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = Customer.objects.create_user(
            username=USER_NAME, email=EMAIL, password=PASSWORD
        )
        self.refresh_token = self.user.tokens()["refresh"]
        self.access_token = self.user.tokens()["access"]
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)

    def test_forgot_password(self) -> None:
        bad_response = self.client.post(
            "/api/forgot-password/", data={"email": "help@mail.ru"}
        )
        correct_response = self.client.post(
            "/api/forgot-password/", data={"email": EMAIL}
        )
        self.assertEquals(correct_response.status_code, 200)
        self.assertEquals(bad_response.status_code, 400)

    def test_change_password(self) -> None:
        bad_response = self.client.put(
            "/api/change-password/",
            data={
                "old_password": PASSWORD,
                "new_password": "white",
                "confirmation_password": "whitesnake",
            },
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        correct_response = self.client.put(
            "/api/change-password/",
            data={
                "old_password": PASSWORD,
                "new_password": "whitesnake",
                "confirmation_password": "whitesnake",
            },
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        test_user = Customer.objects.get(
            email=EMAIL
        )  # получаем польхователя, чтобы проверить смену пароля
        self.assertEquals(correct_response.status_code, 200)
        self.assertEquals(bad_response.status_code, 400)
        self.assertEquals(test_user.check_password("whitesnake"), True)

    def test_change_username_email(self) -> None:
        bad_response = self.client.put(
            "/api/update-user/",
            data={"username": "YuliaL", "email": "help.mail"},
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        correct_response = self.client.put(
            "/api/update-user/",
            data={"username": "YuliaL", "email": EMAIL},
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(correct_response.status_code, 200)
        self.assertEquals(bad_response.status_code, 400)

    def test_reset_password(self) -> None:
        url = reverse(
            "reset_password", kwargs={"uidb64": self.uidb64, "token": self.token}
        )
        bad_response = self.client.put(
            url, data={"new_password": PASSWORD, "confirmation_password": PASSWORD}
        )
        correct_response = self.client.put(
            url,
            data={"new_password": "whitesnake", "confirmation_password": "whitesnake"},
        )
        self.assertEquals(correct_response.status_code, 200)
        self.assertEquals(bad_response.status_code, 400)

    def test_add_update_personal_info(self) -> None:
        correct_response = self.client.put(
            "/api/personal-info/",
            data={
                "date_birth": "2003-04-27",
                "passport": "MC1111111",
                "balance": "5000",
            },
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        bad_response = self.client.put(
            "/api/personal-info/",
            data={
                "date_birth": "2003-04-27",
                "passport": "MC1111111",
                "balance": "7000",
            },
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(correct_response.status_code, 200)
        self.assertEquals(bad_response.status_code, 403)

    def test_create_offer(self) -> None:
        correct_response = self.client.post(
            "/api/create-offer/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        url = reverse(
            "confirm_offer", kwargs={"uidb64": self.uidb64, "token": self.token}
        )
        bad_response = self.client.post(
            url,
            data={
                "max_price": 150.00,
                "customer": self.user.pk,
                "interested_in_car": 1,
            },
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(correct_response.status_code, 200)
        self.assertEquals(bad_response.status_code, 400)
