from django.contrib import admin

from .models import Batch,Department,Semester,Subject

admin.site.register(Department)
admin.site.register(Batch)
admin.site.register(Semester)
admin.site.register(Subject)