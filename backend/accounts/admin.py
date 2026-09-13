from django.contrib import admin
from .models import AttendeeProfile, EmployeeProfile, ManagerProfile, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "f_name",
        "l_name",
        "role",
        "city",
        "mobile",
        "created_at",
    )
    search_fields = ("email", "f_name", "l_name", "mobile")
    list_filter = ("role", "gender", "city")


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

    @admin.display(description="First Name")
    def get_f_name(self, obj):
        return self._get_user(obj).f_name

    @admin.display(description="Last Name")
    def get_l_name(self, obj):
        return self._get_user(obj).l_name

    @admin.display(description="Email")
    def get_email(self, obj):
        return self._get_user(obj).email


@admin.register(AttendeeProfile)
class AttendeeProfileAdmin(BaseUserProfileAdmin):
    user_relation_field = "attendee"
    list_display = (
        "get_user_id",
        "get_f_name",
        "get_l_name",
        "get_email",
        "points",
    )
    search_fields = (
        "attendee__email",
        "attendee__f_name",
        "attendee__l_name",
    )


@admin.register(ManagerProfile)
class ManagerProfileAdmin(BaseUserProfileAdmin):
    user_relation_field = "manager"
    list_display = (
        "get_user_id",
        "get_f_name",
        "get_l_name",
        "get_email",
        "organization",
        "registration_no",
    )
    search_fields = (
        "manager__email",
        "manager__f_name",
        "organization",
        "registration_no",
    )


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(BaseUserProfileAdmin):
    user_relation_field = "employee"
    list_display = (
        "get_user_id",
        "get_f_name",
        "get_l_name",
        "get_email",
    )
    search_fields = (
        "employee__email",
        "employee__f_name",
        "employee__l_name",
    )