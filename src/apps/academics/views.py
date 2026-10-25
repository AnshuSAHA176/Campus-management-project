from rest_framework import viewsets
from .models import Department, Batch, Semester, Subject
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializer import (
    DepartmentSerializer,
    BatchSerializer,
    SemesterSerializer,
    SubjectSerializer,
    DepartmentSearchSerializer,
    batchSearchSerializer,
    SubjectTitleSerializer,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "teacher" and request.user.is_authenticated


class IsTeacherorAdmin(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return (
            request.user.role == "teacher" or request.user.role == "admin"
        ) and request.user.is_authenticated


class DepartmentViewSet(viewsets.ModelViewSet):

    queryset = Department.objects.prefetch_related("semesters", "batches")
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.request.user.role == "teacher":
            return [IsTeacher()]
        return [IsAdminUser()]


class DeparmentSearch(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSearchSerializer


class BatchViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Batch.objects.select_related("department", "semester")
    serializer_class = BatchSerializer


class SemesterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Semester.objects.select_related("department")
    serializer_class = SemesterSerializer


class SubjectViewSet(viewsets.ModelViewSet):

    queryset = Subject.objects.select_related(
        "department", "semester"
    ).prefetch_related("teachers")

    serializer_class = SubjectSerializer

    def get_permissions(self):

        if self.action == "list":
            return [IsTeacherorAdmin()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == "list":
            return SubjectTitleSerializer
        return SubjectSerializer

    def get_queryset(self):
        queryset = Subject.objects.select_related(
            "department", "semester"
        ).prefetch_related("teachers")

        if self.request.user.role == "teacher":
            teacher = self.request.user.teacher_profile  # adjust to your related name
            return queryset.filter(teachers=teacher)

        return queryset


class BatchSearchView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if not query:
            return Response([])

        batches = Batch.objects.filter(Q(name__icontains=query)).values(
            "id",
            "name",
        )[:10]

        return Response(list(batches))


class SubjectSearch(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if not query:
            return Response([])

        subject = Subject.objects.filter(
            Q(name__icontains=query) | Q(code__icontains=query)
        ).values_list("id", "name", "code")[:10]
        print(subject)
        return Response(list(subject))


class BatchAllTItleView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = batchSearchSerializer
    queryset = (
        Batch.objects.only(
            "id",
            "is_active",
            "department_id",
            "department__id",
            "department__name",
            "semester_id",
            "semester__id",
            "semester__name",
        )
        .select_related("department", "semester")
        .filter(is_active=True)
    )
