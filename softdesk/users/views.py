from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.username = f'User {instance.id} deleted'
        instance.email = f'user.{instance.id}@example.com'
        instance.first_name = ''
        instance.last_name = ''
        instance.age = None
        instance.is_active = False
        instance.is_anonymized = True
        instance.can_be_contacted = False
        instance.can_data_be_shared = False
        instance.set_unusable_password()

        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
