from rest_framework.serializers import (
    ModelSerializer,
    SlugRelatedField,
    ValidationError
)

from .models import Project, Contributor, Issue, Comment
from users.models import User


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project

        fields = [
            'id',
            'name',
            'description',
            'project_type',
            'created_time',
            'author',
        ]

        read_only_fields = [
            'created_time',
            'author',
        ]


class ContributorSerializer(ModelSerializer):

    username = SlugRelatedField(
        source='user',
        slug_field='username',
        queryset=User.objects.filter(
            is_active=True,
            is_anonymized=False,
        ),
    )

    class Meta:
        model = Contributor

        fields = [
            'id',
            'username',
            'project',
            'created_time',
        ]

        read_only_fields = [
            'created_time',
            'project',
        ]


class IssueSerializer(ModelSerializer):
    assigned_to = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(
            is_active=True,
            is_anonymized=False,
        ),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Issue

        fields = [
            'id',
            'title',
            'description',
            'priority',
            'issue_type',
            'status',
            'created_time',
            'project',
            'author',
            'assigned_to'
        ]

        read_only_fields = [
            'created_time',
            'project',
            'author',
        ]

    def validate_assigned_to(self, value):
        if value is None:
            return value

        project = self.context['project']

        if not Contributor.objects.filter(
            user=value,
            project=project
        ).exists():
            raise ValidationError(
                f"User {value.username} is not a contributor of the project."
            )

        return value


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment

        fields = [
            'id',
            'description',
            'created_time',
            'issue',
            'author',
        ]

        read_only_fields = [
            'created_time',
            'author',
            'issue',
        ]
