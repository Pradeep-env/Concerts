from rest_framework import serializers
from .models import AttendeeProfile, EmployeeProfile, ManagerProfile, User

BASE_PROFILE_FIELDS = [
    "f_name",
    "l_name",
    "age",
    "gender",
    "city",
    "mobile",
]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "role", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AttendeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendeeProfile
        fields = BASE_PROFILE_FIELDS + ["points"]
        read_only_fields = ["points"]


class ManagerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerProfile
        fields = BASE_PROFILE_FIELDS + [
            "organization",
            "bank_details",
            "registration_no",
            "license",
        ]


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = BASE_PROFILE_FIELDS + [
            "experience",
            "bank_details",
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)