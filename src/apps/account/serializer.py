from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'role',
            'full_name',
            'phone_number',
            'password',
        ]

        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            'email': {
                'required': True,
                'allow_blank': False
            }
        }

    def create(self, validated_data):
        user = User.create_user(**validated_data)
        return user