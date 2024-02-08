from django.urls import path
from Customer.views import *


urlpatterns = [
    path("register/", RegisterViewSet.as_view({"post": "create"}), name="registration"),
    path(
        "confirm-email/<str:uidb64>/<str:token>",
        UserConfirmEmailViewSet.as_view({"get": "retrieve"}),
        name="confirm_email",
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "change-password/",
        ChangePasswordViewSet.as_view({"put": "update"}),
        name="change_password",
    ),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path(
        "reset-password/<str:uidb64>/<str:token>",
        ResetPasswordViewSet.as_view({"put": "update"}),
        name="reset_password",
    ),
    path(
        "update-user/",
        UpdateUsernameEmailViewSet.as_view({"put": "update"}),
        name="update_user",
    ),
]
