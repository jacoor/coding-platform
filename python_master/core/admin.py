# Register your models here.
from typing import ClassVar

from django.contrib import admin

from core.models import EducationPath, Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "difficulty", "created_at", "updated_on")
    search_fields = ("title", "difficulty", "description")
    list_filter = ("difficulty", "created_at", "updated_on")


admin.site.register(Task, TaskAdmin)


class TaskInline(admin.TabularInline):
    model = EducationPath.tasks.through
    extra = 1


class EducationPathAdmin(admin.ModelAdmin):
    list_display = ("name", "difficulty", "created_at", "updated_at")
    search_fields = ("name", "difficulty", "description")
    list_filter = ("difficulty", "created_at", "updated_at")
    inlines: ClassVar = [TaskInline]


admin.site.register(EducationPath, EducationPathAdmin)
