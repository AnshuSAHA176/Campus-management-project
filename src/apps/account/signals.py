from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import User,Student,Teacher
from django.core.cache import cache


@receiver(post_save,sender=User)
def createProfiles(sender,instance,created,**kwargs):
    if created:
        if instance.role  == User.RoleChoices.STUDENT:
            Student.objects.create(user=instance)
        elif instance.role  == User.RoleChoices.TEACHER:
            Teacher.objects.create(user = instance)



@receiver([post_save,post_delete],sender=User)
def cache_delete(sender,instance,**kwargs):
    cache.delete('dashboard')
    