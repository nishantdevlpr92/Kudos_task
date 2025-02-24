from django.contrib import admin
from kudos.models import User, Kudos, Organization
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("organization", "remaining_kudos")}),
    )
    list_display = ("username", "email", "organization", "remaining_kudos", "is_staff", "is_active")
    list_filter = ("organization", "is_staff", "is_active")

admin.site.register(User, CustomUserAdmin)

admin.site.register(Kudos)
admin.site.register(Organization)
