from rest_framework import serializers
from .models import ClassSession

from django.utils import timezone


class ClassSeasionTitleSerializer(serializers.ModelSerializer):
    teacher_picture = serializers.ImageField(source = 'teacher.profile_picture')
    class Meta:
        model = ClassSession
        fields = [
            'id',
            'teacher',
            'room',
            'start_time',
            'teacher_picture'
        ]



class ClassSeasionSerializer(serializers.ModelSerializer):
    teacher_picture = serializers.ImageField(source = 'teacher.profile_picture')
    class Meta:
        model = ClassSession
        fields = '__all__'


    def validate(self, attrs):
        request = self.context.get('request')
        if not request.user.is_staff:
            if attrs['start_time'] > timezone.now().time:
                raise serializers.ValidationError('start time can not be past')

        if attrs['start_time'] > attrs['end_time']

