from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AttendeeProfile, EmployeeProfile, ManagerProfile
from .serializers import (
    AttendeeProfileSerializer,
    EmployeeProfileSerializer,
    LoginSerializer,
    ManagerProfileSerializer,
    UserSerializer,
)

User = get_user_model()


def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["role"] = user.role
    refresh.access_token["role"] = user.role

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def userlist(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup_user(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    return Response(
        {
            "message": "User registered successfully.",
            "user_id": user.id,
            "role": user.role,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def complete_profile(request):
    user = request.user

    role_handlers = {
        "user": (AttendeeProfile, AttendeeProfileSerializer, "Attendee", "attendee"),
        "manager": (ManagerProfile, ManagerProfileSerializer, "Manager", "manager"),
        "employee": (EmployeeProfile, EmployeeProfileSerializer, "Employee", "employee"),
    }

    if user.role not in role_handlers:
        return Response(
            {"error": f"Invalid role: {user.role}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    profile_model, serializer_class, role_label, fk_field = role_handlers[user.role]
    
    profile = profile_model.objects.filter(**{fk_field: user}).first()

    if request.method == "GET":
        if not profile:
            return Response(
                {"error": "Profile not found. Please complete setup first."},
                status=status.HTTP_404_NOT_FOUND,
            )
            
        serializer = serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        if profile:
            return Response(
                {"error": "Profile already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(**{fk_field: user})

        return Response(
            {"message": f"{role_label} profile created", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    ROLE_HANDLERS = {
        "user": (AttendeeProfile, AttendeeProfileSerializer, "Attendee", "attendee"),
        "manager": (ManagerProfile, ManagerProfileSerializer, "Manager", "manager"),
        "employee": (EmployeeProfile, EmployeeProfileSerializer, "Employee", "employee"),
    }
    user = request.user

    if user.role not in ROLE_HANDLERS:
        return Response(
            {"error": f"Invalid role: {user.role}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    profile_model, serializer_class, role_label, fk_field = ROLE_HANDLERS[
        user.role
    ]

    try:
        profile = profile_model.objects.get(**{fk_field: user})
    except profile_model.DoesNotExist:
        return Response(
            {"error": "Profile not found. Please create it first."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = serializer_class(profile, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        {"message": f"{role_label} profile updated", "data": serializer.data},
        status=status.HTTP_200_OK,
    )

@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    user = authenticate(request, username=email, password=password)

    if user is None:
        return Response(
            {"error": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    tokens = generate_tokens_for_user(user)

    return Response(
        {
            "message": "Login successful",
            "tokens": tokens,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "role": user.role,
            },
        },
        status=status.HTTP_200_OK,
    )