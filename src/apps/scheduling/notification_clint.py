from celery import shared_task
import time

@shared_task(bind=True,ignore_result=True)
def wanotification(self):
    time.sleep(10)
    return 'done'