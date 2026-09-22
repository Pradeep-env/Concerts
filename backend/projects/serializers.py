from rest_framework import serializers
from .models import Project, ProjectStats, TeamMate, ProjectChat, Task


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "status",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class ProjectStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStats
        fields = [
            "completed_milestones",
            "total_milestones",
            "more_info",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]


class TeamMateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMate
        fields = [
            "role",
            "agreement",
            "joined_on",
        ]
        read_only_fields = ["joined_on"]


class ProjectChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectChat
        fields = [
            "author",
            "sent_on",
            "message_type",
            "reply_to",
            "message",
        ]
        read_only_fields = ["sent_on"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "assigned_to",
            "assigned_on",
            "expected_on",
            "status",
        ]
        read_only_fields = ["assigned_on"]