from rest_framework import viewsets
from .models import Department,Batch,Semester
from rest_framework.permissions import IsAdminUser
from .serializer import DepartmentSerializer,BatchSerializer,SemesterSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Department.objects.prefetch_related('semesters','batches')
    serializer_class = DepartmentSerializer



class BatchViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Batch.objects.select_related('department','semester')
    serializer_class = BatchSerializer



class SemesterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Semester.objects.select_related('department')
    serializer_class = SemesterSerializer