from django.contrib import admin

from .models import ClassSession,Booking,Timetable

admin.site.register(ClassSession)
admin.site.register(Booking)
admin.site.register(Timetable)