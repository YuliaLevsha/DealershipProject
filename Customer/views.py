from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from Customer.serializers import *
from rest_framework import mixins, status, viewsets, generics, permissions
from django.utils.http import urlsafe_base64_decode
from Customer.tokens import account_activation_token
from Customer.services import send_activation_email
from django.http import HttpRequest
from typing import Any


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Customer.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request: HttpRequest, *args: Any, **kwargs: Dict) -> Response:
        register_serializer = self.serializer_class(data=request.data)
        if register_serializer.is_valid():
            register_serializer.save()
            user = Customer.objects.get(
                email=register_serializer.validated_data.get("email")
            )
            send_activation_email(
                request=request, user=user, action_type="confirm_email"
            )
            return Response(
                {
                    "data": register_serializer.validated_data,
                    "message": "На вашу почту было отправлено сообщение для подтверждения вашей почты",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserConfirmEmailViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):

    def retrieve(self, request: HttpRequest, uidb64: str, token: str) -> Response:
        uid = urlsafe_base64_decode(uidb64)
        user = Customer.objects.get(pk=uid)
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request: HttpRequest) -> Response:
        login_serializer = self.serializer_class(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        return Response(login_serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request: HttpRequest) -> Response:
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TokenError as ex:
            return Response({"Error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = ChangePasswordSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def update(self, request: HttpRequest) -> Response:
        change_serializer = self.serializer_class(
            data=request.data, context={"request": request}, instance=request.user
        )
        if change_serializer.is_valid() and not request.user.check_password(
            change_serializer.validated_data["new_password"]
        ):
            change_serializer.save()
            return Response(
                {
                    "data": change_serializer.validated_data,
                    "message": "password was changed",
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "new password is old password."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request: HttpRequest) -> Response:
        forgot_serializer = self.serializer_class(data=request.data)
        forgot_serializer.is_valid(raise_exception=True)
        try:
            user = Customer.objects.get(email=forgot_serializer.validated_data["email"])
            send_activation_email(
                request=request, user=user, action_type="reset_password"
            )
            return Response(
                {
                    "data": forgot_serializer.data,
                    "message": "На вашу почту было отправлено сообщение чтобы сменить (восттановить) пароль",
                },
                status=status.HTTP_200_OK,
            )
        except Customer.DoesNotExist:
            return Response(
                {"error": "user with this email doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = ResetPasswordSerializer

    def update(self, request: HttpRequest, uidb64: str, token: str) -> Response:
        uid = urlsafe_base64_decode(uidb64)
        user = Customer.objects.get(pk=uid)
        if user is not None and account_activation_token.check_token(user, token):
            reset_serializer = self.serializer_class(user, data=request.data)
            if reset_serializer.is_valid() and not user.check_password(
                reset_serializer.validated_data["new_password"]
            ):
                reset_serializer.save()
                return Response(
                    {
                        "data": reset_serializer.validated_data,
                        "message": "password was changed",
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "new password is old password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateUsernameEmailViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = UpdateUsernameEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request: HttpRequest, *args: Any, **kwargs: Dict) -> Response:
        update_serializer = self.serializer_class(
            data=request.data, instance=request.user
        )
        if update_serializer.is_valid():
            update_serializer.save()
            return Response(
                {
                    "data": update_serializer.validated_data,
                    "message": "username was changed or (and) email was changed",
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": update_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class AddAndUpdatePersonalInfo(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        personal_info_serializer = self.serializer_class(
            data=request.data, instance=request.user
        )
        if personal_info_serializer.is_valid():
            personal_info_serializer.save()
            return Response(
                personal_info_serializer.validated_data, status=status.HTTP_200_OK
            )
        return Response(
            {"error": personal_info_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ConfirmEmailForOfferAndCreate(generics.GenericAPIView):
    queryset = Offer.objects.all()
    serializer_class = CreateOfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: HttpRequest) -> Response:
        customer = Customer.objects.get(username=request.user)
        if Offer.objects.filter(customer=request.user.pk).exists():
            offer_serializer = self.serializer_class(data=request.data)
            if offer_serializer.is_valid():
                offer_serializer.save()
                return Response(offer_serializer.data, status=status.HTTP_201_CREATED)
            return Response(offer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            send_activation_email(
                request=request, user=customer, action_type="confirm_offer"
            )
            return Response(
                {
                    "message": "На вашу почту было отправлено сообщение для создания offer",
                },
                status=status.HTTP_200_OK,
            )


class CreateFirstOfferViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Offer.objects.all()
    serializer_class = CreateOfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        offer_serializer = self.serializer_class(data=request.data)
        if offer_serializer.is_valid():
            offer_serializer.save()
            return Response(offer_serializer.data, status=status.HTTP_201_CREATED)
        return Response(offer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetOffersViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Offer.objects.all()
    serializer_class = GetOfferSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        
        order_value = self.request.GET.get('order')
        
        if order_value:
            queryset = queryset.order_by(order_value)
        
        return queryset

    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        queryset = Offer.objects.filter(customer=request.user.pk)
        offer_serializer = GetOfferSerializer(queryset, many=True)
        return Response(offer_serializer.data, status=status.HTTP_200_OK)
