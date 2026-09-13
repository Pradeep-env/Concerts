from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    role = models.CharField(max_length=20, default='user')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.f_name
    

class AttendeeProfile(models.Model):
    attendee = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.attendee.f_name} ({self.attendee.email})"

class ManagerProfile(models.Model):
    manager = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    organization = models.CharField(max_length=255)
    bank_details = models.JSONField()
    registration_no = models.CharField(max_length=12)
    license = models.JSONField(null=True, blank=True)
    def __str__(self):
        return f"{self.manager.f_name} ({self.manager.email})"

class EmployeeProfile(models.Model):
    employee = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    experiance = models.JSONField()
    bank_details = models.JSONField()
    def __str__(self):
        return f"{self.employee.f_name} ({self.employee.email})"