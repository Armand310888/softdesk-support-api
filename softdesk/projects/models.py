import uuid
from django.db import models

from django.conf import settings


class Project(models.Model):

    class ProjectType(models.TextChoices):
        BACK_END = "BACK_END", "Back-end"
        FRONT_END = "FRONT_END", "Front-end"
        IOS = "IOS", "iOS"
        ANDROID = "ANDROID", "Android"

    name = models.CharField(
        'Name',
        max_length=128
    )

    description = models.TextField(
        'Description',
        max_length=8192,
        blank=True
    )

    project_type = models.CharField(
        'Project Type',
        max_length=11,
        choices=ProjectType.choices
    )

    created_time = models.DateTimeField(
        'Created Time',
        auto_now_add=True
    )

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='Author'
    )


class Contributor(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'project'],
                name='unique_user_project',
            )
        ]

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE
    )

    created_time = models.DateTimeField(
        auto_now_add=True
    )


class Issue(models.Model):

    class IssuePriority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    class IssueType(models.TextChoices):
        BUG = 'BUG', 'Bug'
        FEATURE = 'FEATURE', 'Feature'
        TASK = 'TASK', 'Task'

    class Status (models.TextChoices):
        TO_DO = 'TO_DO', 'To do'
        IN_PROGRESS = 'IN_PROGRESS', 'In progress'
        FINISHED = 'FINISHED', 'Finished'

    title = models.CharField(
        'Title',
        max_length=128
    )

    description = models.TextField(
        'Description',
        max_length=8192,
        blank=True
    )

    priority = models.CharField(
        'Priority',
        max_length=11,
        choices=IssuePriority.choices
    )

    issue_type = models.CharField(
        'Issue Type',
        max_length=11,
        choices=IssueType.choices
    )

    status = models.CharField(
        'Status',
        max_length=11,
        choices=Status.choices,
        default=Status.TO_DO
    )

    created_time = models.DateTimeField(
        'Created Time',
        auto_now_add=True
    )

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        verbose_name='Project'
    )

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='Author',
        related_name='authored_issues'
    )

    assigned_to = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Assigned to',
        related_name='assigned_issues'
    )


class Comment(models.Model):
    description = models.TextField(
        'Description',
        max_length=8192
    )

    created_time = models.DateTimeField(
        'Created Time',
        auto_now_add=True
    )

    issue = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        verbose_name='Issue'
    )

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='Author'
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
