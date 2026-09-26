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
def beforeclass(self):

    
    now = django_timezone.localtime()

    print("NOW:", now)
    print("TIMEZONE:", now.tzinfo)

    target = now + datetime.timedelta(minutes=15)

    start_time = target.time()

    print("Schedule check:", now)
    print("Looking for classes around:", start_time)

    class_sessions = ClassSession.objects.filter(
        date=now.date(),
        start_time__hour=start_time.hour,
        start_time__minute=start_time.minute,
        status=ClassSession.Status.SCHEDULED,
    ).select_related(
        "batch"
    ).prefetch_related(
        "batch__students"
    )

    for class_session in class_sessions:

        print(
            f"Class found: {class_session.subject} "
            f"at {class_session.start_time}"
        )

        for student in class_session.batch.students.all():
            print(student.phone)

    return "done"