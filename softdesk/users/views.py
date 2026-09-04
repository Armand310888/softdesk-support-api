from typing import Any

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from projects.models import Contributor, Issue
from .models import User
from .permissions import IsSelf, IsNotAuthenticated
from .serializers import UserSerializer
from .throttles import RegistrationRateThrottle, LoginRateThrottle


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self) -> list[Any]:
        if self.action == 'create':
            permission_classes = [IsNotAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsSelf]

        return [permission() for permission in permission_classes]

    def get_throttles(self) -> list[Any]:
        throttles = super().get_throttles()

        if self.action == 'create':
            throttles.append(RegistrationRateThrottle())

        return throttles

    def get_queryset(self) -> Any:
        return User.objects.filter(is_anonymized=False)

    @transaction.atomic
    def destroy(
        self,
        request: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """Anonymize the account and remove its project associations."""
        user = self.get_object()

        Contributor.objects.filter(user=user).delete()
        Issue.objects.filter(assigned_to=user).update(assigned_to=None)

        user.username = f'User {user.id} deleted'
        user.email = f'user.{user.id}@example.com'
        user.first_name = ''
        user.last_name = ''
        user.age = None
        user.is_active = False
        user.is_anonymized = True
        user.can_be_contacted = False
        user.can_data_be_shared = False
        user.set_unusable_password()

        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(
        self,
        request: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class LoginView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]
