from rest_framework.serializers import ModelSerializer, SlugRelatedField

from .models import Project, Contributor
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
