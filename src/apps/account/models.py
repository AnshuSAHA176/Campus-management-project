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
    full_name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=15)
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

