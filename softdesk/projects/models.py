from django.db import models

from django.conf import settings


class Project(models.Model):

    class ProjectType(models.TextChoices):
        BACK_END = "BACK_END", "Back-end"
        FRONT_END = "FRONT_END", "Front-end"
        IOS = "IOS", "iOS"
        ANDROID = "ANDROID", "Android"

    name = models.CharField('Name', max_length=128)

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

    created_time = models.DateTimeField('Created Time', auto_now_add=True)

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
