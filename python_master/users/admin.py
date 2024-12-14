from django.contrib import admin

from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_staff", "is_superuser", "last_login", "last_activity")
    search_fields = ("email",)
    readonly_fields = ("last_login", "last_activity")
    ordering = ("email",)
