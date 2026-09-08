from typing import Any

from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import (
    Project,
    Contributor,
    Issue,
    Comment
)
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)
from .permissions import (
    IsAuthor,
    IsContributor,
    IsProjectAuthor,
    CanManageResource,
)


class ProjectContextMixin:
    def get_project(self) -> Project:
        """Return the project identified by the nested route parameter."""
        return get_object_or_404(
                    Project,
                    pk=self.kwargs.get('project_pk')
                )

    def get_issue(self) -> Issue:
        return get_object_or_404(
            Issue,
            pk=self.kwargs.get('issue_pk'),
            project_id=self.kwargs.get('project_pk'),
    )


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self) -> list[Any]:
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsContributor]
        else:
            permission_classes = [IsAuthenticated, IsContributor, IsAuthor]

        return [permission() for permission in permission_classes]

    def get_queryset(self) -> Any:
        return Project.objects.all()

    @transaction.atomic
    def perform_create(self, serializer: Any) -> None:
        """Create the project and its initial contributor atomically."""
        project = serializer.save(author=self.request.user)

        Contributor.objects.create(
            user=self.request.user,
            project=project,
        )

    @extend_schema(
        summary='Project listing is disabled',
        description='Projects cannot be listed. Use POST on this path to create a project.',
        responses={405: None},
        operation_id='projects_list_disabled'
    )
    def list(
        self,
        request: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ContributorViewSet(ProjectContextMixin, ModelViewSet):
    serializer_class = ContributorSerializer

    http_method_names = ['get', 'post', 'delete']

    def get_permissions(self) -> list[Any]:
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsProjectAuthor]
        else:
            permission_classes = [IsAuthenticated, IsContributor]

        return [permission() for permission in permission_classes]

    def get_queryset(self) -> Any:
        return Contributor.objects.filter(
            project_id=self.kwargs.get('project_pk')
        ).select_related('user')

    def perform_create(self, serializer: Any) -> None:
        """Add an active, non-duplicate contributor to the project."""
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
    def destroy(
        self,
        request: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """Remove a contributor and clear their project assignments."""
        contributor = self.get_object()

        project = self.get_project()

        if contributor.user_id == project.author_id:
            raise PermissionDenied('This action is forbidden.')

        Issue.objects.filter(
            assigned_to=contributor.user,
            project=project
        ).update(assigned_to=None)

        return super().destroy(request, *args, **kwargs)


class IssueViewSet(ProjectContextMixin, ModelViewSet):
    serializer_class = IssueSerializer

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self) -> list[Any]:
        if self.action in ['create', 'retrieve', 'list']:
            permission_classes = [IsAuthenticated, IsContributor]
        else:
            permission_classes = [
                IsAuthenticated,
                IsContributor,
                CanManageResource,
            ]

        return [permission() for permission in permission_classes]

    def get_queryset(self) -> Any:
        project = self.get_project()

        return Issue.objects.filter(
            project=project
        ).select_related(
            'assigned_to',
        )

    def perform_create(self, serializer: Any) -> None:
        """Create an issue for the current project and authenticated user."""
        project = self.get_project()

        serializer.save(
            author=self.request.user,
            project=project
        )

    def get_serializer_context(self) -> dict[str, Any]:
        context = super().get_serializer_context()
        context['project'] = self.get_project()
        return context


class CommentViewSet(ProjectContextMixin, ModelViewSet):
    serializer_class = CommentSerializer

    http_method_names = ['post', 'patch', 'get', 'delete']

    def get_permissions(self) -> list[Any]:
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsContributor]
        elif self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsContributor, IsAuthor]
        else:
            permission_classes = [
                IsAuthenticated,
                IsContributor,
                CanManageResource,
            ]

        return [permission() for permission in permission_classes]

    def get_queryset(self) -> Any:

        issue = self.get_issue()

        return Comment.objects.filter(issue=issue).select_related('issue')

    def perform_create(self, serializer: Any) -> None:
        """Create a comment attached to the issue in the current project."""
        issue = self.get_issue()

        serializer.save(
            author=self.request.user,
            issue=issue
        )
