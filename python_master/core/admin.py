# Register your models here.
from django.contrib import admin
from django.utils.safestring import mark_safe
from core.models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "difficulty", "created_at", "updated_on")
    search_fields = ("title", "difficulty", "description")
    list_filter = ("difficulty", "created_at", "updated_on")


admin.site.register(Task, TaskAdmin)
