from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer

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
            }
        }

    def validate_password(self, value):
        validate_password(value, user=self.instance)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        instance = super().update(instance, validated_data)

        if password is None:
            return instance

        else:
            instance.set_password(password)
            instance.save()
            return instance
