from copy import copy
from typing import Any

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import (
    ValidationError as DjangoValidationError
)
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError as DRFValidationError
)

from users.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'age',
            'can_be_contacted',
            'can_data_be_shared',
            'is_anonymized',
            'created_time',
            'password',
        ]
        read_only_fields = [
            'is_anonymized',
            'created_time',
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
            'age': {
                'required': True,
                'allow_null': False,
            },
            'can_be_contacted': {
                'required': True,
            },
            'can_data_be_shared': {
                'required': True,
            },
            'email': {
                'required': True,
                'allow_null': False,
            }
        }

    def validate(self, data):
        password = data.get('password')

        if password is None:
            return data

        if self.instance is None:
            user = User(**data)

        else:
            user = copy(self.instance)

            for attribute, value in data.items():
                setattr(user, attribute, value)

        try:
            validate_password(
                password,
                user=user,
            )
        except DjangoValidationError as error:
            raise DRFValidationError({
                "password": error.messages
            })

        return data

    def create(self, validated_data: dict[str, Any]) -> User:
        """Create a user while storing the password in hashed form."""
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(
        self,
        instance: User,
        validated_data: dict[str, Any],
    ) -> User:
        """Update the user and hash a new password when one is provided."""
        password = validated_data.pop('password', None)

        instance = super().update(instance, validated_data)

        if password is None:
            return instance

        else:
            instance.set_password(password)
            instance.save()
            return instance
