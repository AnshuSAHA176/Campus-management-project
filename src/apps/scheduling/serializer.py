from rest_framework import serializers
from .models import ClassSession

from django.utils import timezone
from apps.academics.models import Subject

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
            if attrs['start_time'] < timezone.now().time():
                raise serializers.ValidationError(
                    'Start time cannot be in the past.'
                )
            if attrs['date'] < timezone.now().date():
                        raise serializers.ValidationError(
                            'Class date cannot be in the past.'
                        )

        if attrs['start_time'] >= attrs['end_time']:
                raise serializers.ValidationError(
                    'Start time must be before the end time.'
                )

        subject = attrs['subject']

        if subject.department != attrs['department']:
                raise serializers.ValidationError(
                    'The subject does not belong to the department.'
                )

        if subject.semester != attrs['semester']:
                raise serializers.ValidationError(
                    'The subject does not belong to the semester.'
                )

        time_overlape = ClassSession.objects.filter(
              date = attrs['date'],
              start_time__lt = attrs['end_time'],
              end_time__gt=attrs['start_time'],
              
        )
        if self.instance:
            time_overlape = time_overlape.exclude(
                pk=self.instance.pk
            )

        if time_overlape.filter(teacher = attrs['teacher']).exists() :
              
              raise serializers.ValidationError('The teacher already have class that time')
        
        if time_overlape.filter(batch = attrs['batch']).exists():
              
              raise serializers.ValidationError('The batch already have class this time range')
        
        if time_overlape.filter(room = attrs['room']).exists():
              
              raise serializers.ValidationError(f'The room alreay book for this time range {time_overlape.first().start_time} - {time_overlape.first().end_time}')

        if not attrs['room'].is_active or not attrs['teacher'].is_active or not attrs['batch'].is_active or not attrs['subject'].is_active:
              raise serializers.ValidationError('Please check somthing is not active before crate a class seasion')

        if attrs['teacher'].department != attrs['department']:
              
              raise serializers.ValidationError('teacher have to belong to the same department')
        
        if attrs['room'].department != attrs['department']:
              
              raise serializers.ValidationError('room have to belong to the same department')
        
        if attrs['batch'].department != attrs['department']:
              
              raise serializers.ValidationError('teacher have to belong to the same department')



    def create(self, validated_data):
          request = self.context.get('request')

          if request.user.role == 'teacher':
                validated_data['teacher'] = request.user.teacher_profile
                validated_data['department'] = request.user.teacher_profile.department

          validated_data['created_by'] = request.user
          return ClassSession.objects.create(**validated_data)



{
  "department": 1,
  "semester": 3,
  "subject": 5,
  "batch": 2,
  "room": 204,
  "date": "2026-09-28",
  "start_time": "10:00",
  "end_time": "11:00"
}