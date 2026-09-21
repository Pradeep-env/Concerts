from rest_framework import serializers
from .models import AttendeeTicket, Concert, ConcertTicket


class ConcertCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = [
            "id",
            "title",
            "venue",
            "date",
            "artists",
            "description",
            "contact",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class ConcertTicketSerializer(serializers.ModelSerializer):
    tier_display = serializers.CharField(
        source="get_tier_display",
        read_only=True
    )

    class Meta:
        model = ConcertTicket
        fields = [
            "id",
            "tier",
            "tier_display",
            "cost",
            "points",
            "total_quantity",
            "available_quantity",
        ]
        read_only_fields = ["id"]


class AttendeeTicketSerializer(serializers.ModelSerializer):
    tier_display = serializers.CharField(
        source="concert_ticket.get_tier_display",
        read_only=True
    )
    concert_title = serializers.CharField(
        source="concert_ticket.concert.title",
        read_only=True
    )

    class Meta:
        model = AttendeeTicket
        fields = [
            "id",
            "concert_ticket",
            "concert_title",
            "tier_display",
            "status",
            "info",
            "purchased_at",
        ]
        read_only_fields = ["id", "purchased_at"]


class ConcertDetailSerializer(serializers.ModelSerializer):
    tickets = ConcertTicketSerializer(many=True, read_only=True)

    class Meta:
        model = Concert
        fields = [
            "id",
            "title",
            "venue",
            "date",
            "artists",
            "description",
            "contact",
            "status",
            "created_at",
            "tickets",
        ]
        read_only_fields = ["id", "created_at"]