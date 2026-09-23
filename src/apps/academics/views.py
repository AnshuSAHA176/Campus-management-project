from rest_framework import viewsets
from .models import Department
from rest_framework.permissions import IsAdminUser
from .serializer import DepartmentSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer