from rest_framework import serializers
from .models import Department,Batch,Semester


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields ='__all__'


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'
class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'