from rest_framework.serializers import ModelSerializer

from .models import Project


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