from rest_framework import serializers
from .models import Department,Batch,Semester,Subject


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

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            "id",
            "department",
            "semester",
            "teachers",
            "name",
            "code",
            
           
            "is_active",
            "created_at",
            "updated_at",
        ]

class DepartmentSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields=[
            "id",
            "name"
        ]




class batchSearchSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source = 'department.name')
    semester_name = serializers.CharField(source = 'semester.name')
    class Meta:
        model = Batch
        fields=[
            "id",
            'department_name',
            'semester_name'
        ]



