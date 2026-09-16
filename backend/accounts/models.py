from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ("user", "User"),
            ("manager", "Manager"),
            ("employee", "Employee"),
        ],
        default="user",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email} ({self.role})"


class BasePersonalInfo(models.Model):
    f_name = models.CharField(max_length=100, blank=True, default="")
    l_name = models.CharField(max_length=100, blank=True, default="")
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    mobile = models.CharField(max_length=15, blank=True, default="")

    class Meta:
        abstract = True


class AttendeeProfile(BasePersonalInfo):
    attendee = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="attendee_profile",
    )
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.f_name or self.attendee.username} ({self.attendee.email})"


class ManagerProfile(BasePersonalInfo):
    manager = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="manager_profile",
    )
    organization = models.CharField(max_length=255)
    bank_details = models.JSONField(default=dict, blank=True)
    registration_no = models.CharField(max_length=50)
    license = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.organization} - {self.manager.email}"


class EmployeeProfile(BasePersonalInfo):
    employee = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="employee_profile",
    )
    experience = models.JSONField(default=dict, blank=True)
    bank_details = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.f_name or self.employee.username} ({self.employee.email})"