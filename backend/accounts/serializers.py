from rest_framework import serializers
from .models import User, AttendeeProfile, ManagerProfile, EmployeeProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}


class AttendeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendeeProfile
        fields = ["points"]


class ManagerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerProfile
        fields = ["organization", "bank_details", "registration_no", "license"]


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ["experiance", "bank_details"]