from rest_framework.decorators import api_view,permission_classes
from .models import User, AttendeeProfile, ManagerProfile, EmployeeProfile
from .serializers import UserSerializer, AttendeeProfileSerializer, ManagerProfileSerializer, EmployeeProfileSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(["GET"])
def userlist(request):
    Users = User.objects.all()
    serializer = UserSerializer(Users, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([AllowAny])
def signup_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        raw_password = serializer.validated_data.get("password")
        user = serializer.save(password=make_password(raw_password))

        return Response(
            {
                "message": "User registered Successfully.",
                "user_id": str(user.id),
                "role": user.role,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def complete_profile(request):
    user_id = request.data.get("user_id")
    if not user_id:
        return Response(
            {"error": "user_id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if user.role == "user":
        if AttendeeProfile.objects.filter(attendee=user).exists():
            return Response(
                {"error": "Profile already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = AttendeeProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(attendee=user)
            return Response(
                {"message": "Attendee profile created"},
                status=status.HTTP_201_CREATED,
            )

    elif user.role == "manager":
        if ManagerProfile.objects.filter(manager=user).exists():
            return Response(
                {"error": "Profile already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = ManagerProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(manager=user)
            return Response(
                {"message": "Manager profile created"},
                status=status.HTTP_201_CREATED,
            )

    elif user.role == "employee":
        if EmployeeProfile.objects.filter(employee=user).exists():
            return Response(
                {"error": "Profile already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = EmployeeProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=user)
            return Response(
                {"message": "Employee profile created"},
                status=status.HTTP_201_CREATED,
            )

    else:
        return Response(
            {"error": f"Invalid role: {user.role}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    refresh["role"] = user.role
    refresh["user_id"] = str(user.id)

    access = refresh.access_token
    access["role"] = user.role
    access["user_id"] = str(user.id)

    return {"refresh": str(refresh), "access": str(access)}

@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not check_password(password, user.password):
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
                "id": str(user.id),
                "email": user.email,
                "role": user.role,
                "f_name": user.f_name,
                "l_name": user.l_name,
            },
        },
        status=status.HTTP_200_OK,
    )