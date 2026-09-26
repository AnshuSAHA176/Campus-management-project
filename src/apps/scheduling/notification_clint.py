from celery import shared_task
import time
from .models import ClassSession
from django.utils import timezone as django_timezone
import datetime

@shared_task(bind=True,ignore_result=True)
def wanotification(self):
    time.sleep(10)
    return 'done'



from .models import ClassSession


@shared_task(bind=True, ignore_result=True)
def beforeclass(self,instance_id):

    
    class_seasion = ClassSession.objects.select_related('teacher').get(id = instance_id)

    if class_seasion.status != ClassSession.Status.SCHEDULED:
        return 'class is not longer sheduld'
    
    print( class_seasion.teacher.phone)

    print("15 MINUTES BEFORE CLASS")
    print(class_seasion.id)
    return "done"