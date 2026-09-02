from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from .models import Project, Contributor, Issue, Comment


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsProjectAuthor(BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(
            Project,
            pk=view.kwargs.get('project_pk'),
        )

        return request.user == project.author


class IsContributor(BasePermission):
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')

        if project_pk is None:
            return True

        return Contributor.objects.filter(
            user=request.user,
            project_id=project_pk
        ).exists()

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            project = obj

        elif isinstance(obj, Issue):
            project = obj.project

        elif isinstance(obj, Comment):
            project = obj.issue.project

        return Contributor.objects.filter(
            user=request.user,
            project=project,
        ).exists()
