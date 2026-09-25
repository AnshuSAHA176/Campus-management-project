from rest_framework import serializers
from .models import User,Student,Teacher
from django.contrib.auth import authenticate
from apps.scheduling.models import  Activity

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'role',
           
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
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(write_only = True)

    
    def validate(self, attrs):
        if attrs['email'] is None:
            raise serializers.ValidationError('email is required')
        if attrs['password'] is None:
            raise serializers.ValidationError('password is required')

        user = authenticate(email = attrs['email'],password = attrs ['password'])

        if user is None:
            raise serializers.ValidationError('email and password is wrong')

        attrs['user'] = user
        return attrs

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields =[
            'student_id',
            'batch',
            'phone',
            'full_name',
            'enrollment_date',
            'profile_picture'
        ]
class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields =[
            'employee_id',
            'department',
            'designation',
            'phone',
            'profile_picture'
        ]


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields ='__all__'