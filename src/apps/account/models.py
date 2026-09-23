from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
import uuid
from .custom_manager import CustomeUsermanager
from django.contrib.auth.models import PermissionsMixin


class User(AbstractBaseUser,PermissionsMixin):
    class RoleChoices(models.TextChoices):
        STUDENT=('student','student')
        Teacher=('teacher','Teacher')
        ADMIN=('admin','Admin')
        HOD=('hod','HOD')

 
    objects  = CustomeUsermanager()
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user_name = None
    email = models.EmailField(

         verbose_name="email address",
        max_length=255,
        unique=True,
    )
    role = models.CharField(
        max_length=200,
        choices=RoleChoices.choices,
        default=RoleChoices.STUDENT
        )
    
    USERNAME_FIELD = "email"
    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    
    
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = []




class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    
    student_id = models.CharField(max_length=50, unique=True)
    batch = models.ForeignKey(
        "academics.Batch",
        on_delete=models.PROTECT,
        related_name="students",
        null=True
    )
    full_name = models.CharField(max_length=300,blank=True)
    phone = models.CharField(max_length=20, blank=True)
    enrollment_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name}"


class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_profile"
    )

    employee_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=300,blank=True)
    
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.PROTECT,
        related_name="teachers",
        null=True
    )

    designation = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.full_name}"