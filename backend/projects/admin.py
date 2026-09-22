from django.contrib import admin
from .models import Project, ProjectChat, ProjectStats, Task, TeamMate


class TeamMateInline(admin.TabularInline):
    model = TeamMate
    extra = 1
    fields = ("employee", "role", "joined_on")
    readonly_fields = ("joined_on",)
    autocomplete_fields = ("employee",)


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    fields = ("title", "assigned_to", "status", "expected_on")
    show_change_link = True


class ProjectStatsInline(admin.StackedInline):
    model = ProjectStats
    can_delete = False
    extra = 0
    fields = ("completed_milestones", "total_milestones", "more_info")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "get_concert_title",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "title",
        "concert__title",
        "concert__manager__organization",
    )
    ordering = ("-created_at",)
    inlines = [TeamMateInline, TaskInline, ProjectStatsInline]

    @admin.display(description="Concert")
    def get_concert_title(self, obj):
        return obj.concert.title


@admin.register(TeamMate)
class TeamMateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_employee_email",
        "role",
        "get_project_title",
        "joined_on",
    )
    list_filter = ("role", "joined_on")
    search_fields = (
        "employee__employee__email",
        "employee__f_name",
        "employee__l_name",
        "project__title",
        "role",
    )
    ordering = ("-joined_on",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("employee__employee", "project")
        )

    @admin.display(description="Employee Email")
    def get_employee_email(self, obj):
        return obj.employee.employee.email

    @admin.display(description="Project")
    def get_project_title(self, obj):
        return obj.project.title


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "get_project_title",
        "get_assigned_member",
        "status",
        "expected_on",
        "assigned_on",
    )
    list_filter = ("status", "assigned_on", "expected_on")
    search_fields = (
        "title",
        "description",
        "project__title",
        "assigned_to__employee__f_name",
        "assigned_to__employee__l_name",
    )
    ordering = ("-assigned_on",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("project", "assigned_to__employee__employee")
        )

    @admin.display(description="Project")
    def get_project_title(self, obj):
        return obj.project.title

    @admin.display(description="Assigned To")
    def get_assigned_member(self, obj):
        if obj.assigned_to:
            return f"{obj.assigned_to.employee.f_name} ({obj.assigned_to.role})"
        return "Unassigned"


@admin.register(ProjectChat)
class ProjectChatAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project",
        "author",
        "message_type",
        "short_message",
        "reply_to",
        "sent_on",
    )
    list_filter = ("message_type", "sent_on")
    search_fields = ("author__username", "author__email", "message", "project__title")
    readonly_fields = ("sent_on",)
    ordering = ("-sent_on",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("project", "author", "reply_to")

    @admin.display(description="Message")
    def short_message(self, obj):
        return (obj.message[:50] + "...") if len(obj.message) > 50 else obj.message


@admin.register(ProjectStats)
class ProjectStatsAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "completed_milestones",
        "total_milestones",
        "updated_at",
    )
    search_fields = ("project__title",)