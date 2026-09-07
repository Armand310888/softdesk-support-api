from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from .models import Project, Contributor, Issue, Comment


class IsAuthor(BasePermission):
    def has_object_permission(
        self,
        request: Any,
        view: Any,
        obj: Any,
    ) -> bool:
        return obj.author_id == request.user.id


class IsProjectAuthor(BasePermission):
    def has_permission(self, request: Any, view: Any) -> bool:
        project = get_object_or_404(
            Project,
            pk=view.kwargs.get('project_pk'),
        )

        return request.user.id == project.author_id


class CanManageResource(BasePermission):
    def has_object_permission(
        self,
        request: Any,
        view: Any,
        obj: Any,
    ) -> bool:
        """Allow the resource author or project author when needed."""
        if obj.author_id == request.user.id:
            return True

        project = get_object_or_404(
            Project,
            pk=view.kwargs.get('project_pk'),
        )

        return (
            request.user.id == project.author_id
            and not Contributor.objects.filter(
                user_id=obj.author_id,
                project_id=project.id
            ).exists()
        )


class IsContributor(BasePermission):
    def has_permission(self, request: Any, view: Any) -> bool:
        project_pk = view.kwargs.get('project_pk')

        if project_pk is None:
            return True

        return Contributor.objects.filter(
            user_id=request.user.id,
            project_id=project_pk
        ).exists()

    def has_object_permission(
        self,
        request: Any,
        view: Any,
        obj: Any,
    ) -> bool:
        """Check whether the user contributes to the object's project."""
        if isinstance(obj, Project):
            project_id = obj.id

        elif isinstance(obj, Issue):
            project_id = obj.project_id

        elif isinstance(obj, Comment):
            project_id = obj.issue.project_id

        return Contributor.objects.filter(
            user_id=request.user.id,
            project_id=project_id,
        ).exists()
