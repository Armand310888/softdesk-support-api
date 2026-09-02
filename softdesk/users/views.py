from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from projects.models import Contributor, Issue
from .models import User
from .permissions import IsSelf
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsSelf]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return User.objects.filter(is_anonymized=False)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
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

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
