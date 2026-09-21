from django.db import models
from accounts.models import AttendeeProfile, ManagerProfile


class Concert(models.Model):
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("live", "Live"),
        ("canceled", "Canceled"),
    ]

    manager = models.ForeignKey(
        ManagerProfile,
        on_delete=models.CASCADE,
        related_name="concerts",
    )
    title = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    date = models.DateTimeField()
    artists = models.JSONField(default=list)
    description = models.TextField(blank=True, default="")
    contact = models.JSONField(default=dict)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="upcoming",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.manager.organization}"


class ConcertTicket(models.Model):
    TIER_CHOICES = [
        ("tier3", "Normal"),
        ("tier2", "Special"),
        ("tier1", "Elite"),
        ("tier0", "VIP"),
    ]

    concert = models.ForeignKey(
        Concert,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    tier = models.CharField(
        max_length=20,
        choices=TIER_CHOICES,
        default="tier3",
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    points = models.PositiveIntegerField(default=0)
    total_quantity = models.PositiveIntegerField(default=100)
    available_quantity = models.PositiveIntegerField(default=100)

    class Meta:
        unique_together = ("concert", "tier")

    def __str__(self):
        return f"{self.concert.title} - {self.get_tier_display()}"


class AttendeeTicket(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("used", "Used"),
        ("expired", "Expired"),
        ("canceled", "Canceled"),
    ]

    attendee = models.ForeignKey(
        AttendeeProfile,
        on_delete=models.CASCADE,
        related_name="purchased_tickets",
    )
    concert_ticket = models.ForeignKey(
        ConcertTicket,
        on_delete=models.CASCADE,
        related_name="attendee_passes",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
    )
    info = models.JSONField(default=dict, blank=True)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attendee} - {self.concert_ticket.concert.title} ({self.status})"

