from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import AttendeeTicket, Concert, ConcertTicket
from .serializers import (
    AttendeeTicketSerializer,
    ConcertCreateSerializer,
    ConcertDetailSerializer,
    ConcertTicketSerializer,
)


def can_user_modify_concert(user, concert):
    if user.role == "manager" and hasattr(user, "manager_profile"):
        return concert.manager_id == user.manager_profile.pk
    return False


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_concert(request):
    if request.user.role != "manager" or not hasattr(request.user, "manager_profile"):
        return Response(
            {"error": "Only verified managers can create concerts."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = ConcertCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    concert = serializer.save(manager=request.user.manager_profile)

    return Response(
        {
            "message": "New concert created successfully",
            "data": ConcertCreateSerializer(concert).data,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def concert_detail_action(request, pk):
    concert = get_object_or_404(Concert, pk=pk)

    if not can_user_modify_concert(request.user, concert):
        return Response(
            {"error": "You do not have permission to modify or delete this concert."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "PATCH":
        serializer = ConcertCreateSerializer(concert, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Concert updated successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    elif request.method == "DELETE":
        concert.delete()
        return Response(
            {"message": "Concert deleted successfully"},
            status=status.HTTP_200_OK,
        )