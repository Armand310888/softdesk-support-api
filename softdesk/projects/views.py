from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import (
    Project,
    Contributor,
    Issue
)
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer
)
from .permissions import (
    IsAuthor,
    IsContributor,
    IsProjectAuthor,
)


class ProjectContextMixin:
    def get_project(self):
        return get_object_or_404(
                    Project,
                    pk=self.kwargs.get('project_pk')
                )


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsContributor]
        else:
            permission_classes = [IsAuthenticated, IsAuthor]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Project.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)

        Contributor.objects.create(
            user=self.request.user,
            project=project,
        )

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ContributorViewSet(ProjectContextMixin, ModelViewSet):
    serializer_class = ContributorSerializer

    http_method_names = ['get', 'post', 'delete']

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsProjectAuthor]
        else:
            permission_classes = [IsAuthenticated, IsContributor]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Contributor.objects.filter(
            project_id=self.kwargs.get('project_pk')
        )

    def perform_create(self, serializer):
        project = self.get_project()
        user = serializer.validated_data['user']

        if Contributor.objects.filter(
            user=user,
            project=project,
        ).exists():
            raise ValidationError(
                f"User {user.username} is already contributor to this project."
            )

        serializer.save(project=project)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        contributor = self.get_object()

        project = self.get_project()

        if contributor.user == project.author:
            raise PermissionDenied('This action is forbidden.')

        Issue.objects.filter(
            assigned_to=contributor.user,
            project=project
        ).update(assigned_to=None)

        return super().destroy(request, *args, **kwargs)


class IssueViewSet(ProjectContextMixin, ModelViewSet):
    serializer_class = IssueSerializer

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ['create', 'retrieve', 'list']:
            permission_classes = [IsAuthenticated, IsContributor]
        else:
            permission_classes = [IsAuthenticated, IsContributor, IsAuthor]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Issue.objects.filter(
            project_id=self.kwargs.get('project_pk')
        )

    def perform_create(self, serializer):
        project = self.get_project()

        serializer.save(
            author=self.request.user,
            project=project
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project'] = self.get_project()
        return context
