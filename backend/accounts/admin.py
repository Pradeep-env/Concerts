from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import AttendeeProfile, EmployeeProfile, ManagerProfile, User


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "role",
        "is_active",
        "is_staff",
        "created_at",
    )
    search_fields = ("email", "username")
    list_filter = ("role", "is_active", "is_staff", "created_at")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("email",)}),
        ("Role & Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created_at")}),
    )
    readonly_fields = ("created_at", "last_login")


class BaseUserProfileAdmin(admin.ModelAdmin):
    user_relation_field = None

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(self.user_relation_field)
        )

    def _get_user(self, obj):
        return getattr(obj, self.user_relation_field)

    @admin.display(description="User ID")
    def get_user_id(self, obj):
        return self._get_user(obj).id

    @admin.display(description="Email")
    def get_email(self, obj):
        return self._get_user(obj).email


@admin.register(AttendeeProfile)
class AttendeeProfileAdmin(BaseUserProfileAdmin):
    user_relation_field = "attendee"
    list_display = (
        "get_user_id",
        "get_email",
        "f_name",
        "l_name",
        "city",
        "mobile",
        "points",
    )
    search_fields = (
        "attendee__email",
        "f_name",
        "l_name",
        "mobile",
        "city",
    )
    list_filter = ("city", "gender")


@admin.register(ManagerProfile)
class ManagerProfileAdmin(BaseUserProfileAdmin):
    user_relation_field = "manager"
    list_display = (
        "get_user_id",
        "get_email",
        "f_name",
        "l_name",
        "organization",
        "registration_no",
        "city",
    )
    search_fields = (
        "manager__email",
        "f_name",
        "l_name",
        "organization",
        "registration_no",
    )
    list_filter = ("city",)


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(BaseUserProfileAdmin):
    user_relation_field = "employee"
    list_display = (
        "get_user_id",
        "get_email",
        "f_name",
        "l_name",
        "city",
        "mobile",
    )
    search_fields = (
        "employee__email",
        "f_name",
        "l_name",
        "mobile",
    )
    list_filter = ("city", "gender")