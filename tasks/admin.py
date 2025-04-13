from django.contrib import admin
from .models import tasks

class tasksadmin(admin.ModelAdmin):
    readonly_fields = ('created',)

#Register your models here.
admin.site.register(tasks, tasksadmin)