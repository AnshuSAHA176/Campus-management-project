from rest_framework import viewsets
from .models import Department,Batch,Semester,Subject
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .serializer import DepartmentSerializer,BatchSerializer,SemesterSerializer,SubjectSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q


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

class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Subject.objects.select_related('department','semester').prefetch_related('teachers')
                                              

    serializer_class = SubjectSerializer

class BatchSearchView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if not query:
            return Response([])

        batches = Batch.objects.filter(
            Q(name__icontains=query)
        ).values(
            "id",
            "name",
        )[:10]

        return Response(list(batches))