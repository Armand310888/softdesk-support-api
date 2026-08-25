from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    age = models.SmallIntegerField(validators=[MinValueValidator(15)])

    can_be_contacted = models.BooleanField(default=False)

    can_data_be_shared = models.BooleanField(default=False)

    created_time = models.DateTimeField(auto_now_add=True)

    email = models.EmailField(unique=True)

    is_anonymized = models.BooleanField(default=True)

    REQUIRED_FIELDS = ["email", "age"]
