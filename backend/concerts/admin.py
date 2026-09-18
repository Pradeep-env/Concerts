from django.contrib import admin
from .models import AttendeeTicket, Concert, ConcertTicket


class ConcertTicketInline(admin.TabularInline):
    model = ConcertTicket
    extra = 1
    fields = (
        "tier",
        "cost",
        "points",
        "total_quantity",
        "available_quantity",
    )


@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "get_manager_organization",
        "venue",
        "date",
        "status",
        "created_at",
    )
    list_filter = ("status", "date", "created_at")
    search_fields = (
        "title",
        "venue",
        "manager__organization",
        "manager__manager__email",
    )
    ordering = ("-date",)
    inlines = [ConcertTicketInline]

    @admin.display(description="Organization")
    def get_manager_organization(self, obj):
        return obj.manager.organization


@admin.register(ConcertTicket)
class ConcertTicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "concert",
        "tier",
        "cost",
        "points",
        "available_quantity",
        "total_quantity",
    )
    list_filter = ("tier", "concert__status")
    search_fields = ("concert__title", "tier")
    ordering = ("concert", "tier")


@admin.register(AttendeeTicket)
class AttendeeTicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_attendee_email",
        "get_concert_title",
        "get_tier",
        "status",
        "purchased_at",
    )
    list_filter = ("status", "purchased_at", "concert_ticket__tier")
    search_fields = (
        "attendee__attendee__email",
        "attendee__f_name",
        "attendee__l_name",
        "concert_ticket__concert__title",
    )
    readonly_fields = ("purchased_at",)
    ordering = ("-purchased_at",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "attendee__attendee",
                "concert_ticket__concert",
            )
        )

    @admin.display(description="Attendee Email")
    def get_attendee_email(self, obj):
        return obj.attendee.attendee.email

    @admin.display(description="Concert")
    def get_concert_title(self, obj):
        return obj.concert_ticket.concert.title

    @admin.display(description="Tier")
    def get_tier(self, obj):
        return obj.concert_ticket.get_tier_display()