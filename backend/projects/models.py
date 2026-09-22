from accounts.models import EmployeeProfile, User
from concerts.models import Concert
from django.db import models


class Project(models.Model):
    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]

    concert = models.OneToOneField(
        Concert,
        on_delete=models.CASCADE,
        related_name="project",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ongoing",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.concert.title})"


class TeamMate(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="members",
    )
    employee = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name="project_assignments",
    )
    role = models.CharField(
        max_length=100
    )
    agreement = models.JSONField(default=dict, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "employee")

    def __str__(self):
        return f"{self.employee} - {self.role} in {self.project.title}"


class ProjectChat(models.Model):
    MESSAGE_TYPES = [
        ("text", "Text"),
        ("file", "File"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="chats",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="project_messages",
    )
    sent_on = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPES,
        default="text",
    )

    reply_to = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="replies",
    )
    message = models.TextField()

    class Meta:
        ordering = ["sent_on"]

    def __str__(self):
        return f"{self.author.username} at {self.sent_on}: {self.message[:30]}"


class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=255, default="New Task")
    description = models.TextField(blank=True, default="")
    assigned_to = models.ForeignKey(
        TeamMate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    assigned_on = models.DateTimeField(auto_now_add=True)
    expected_on = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    def __str__(self):
        return f"{self.title} [{self.status}] - {self.project.title}"


class ProjectStats(models.Model):
    
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name="stats",
    )
    completed_milestones = models.PositiveIntegerField(default=0)
    total_milestones = models.PositiveIntegerField(default=0)
    more_info = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stats for {self.project.title}"