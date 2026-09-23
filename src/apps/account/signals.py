from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,Student,Teacher

@receiver(post_save,sender=User)
def createProfiles(sender,instance,created,**kwargs):
    if created:
        if instance.role  == User.RoleChoices.STUDENT:
            Student.objects.create(user=instance)
        elif instance.role  == User.RoleChoices.TEACHER:
            Teacher.objects.create(user = instance)