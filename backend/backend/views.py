from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])  # Health checks must be publicly accessible
def health_check(request):
    health_status = {"status": "healthy", "database": "disconnected"}

    try:
        # Execute a minimal query to verify database connectivity
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
        health_status["database"] = "connected"
        return Response(health_status, status=status.HTTP_200_OK)
    except Exception as exc:
        health_status["status"] = "unhealthy"
        health_status["error"] = str(exc)
        return Response(
            health_status, status=status.HTTP_503_SERVICE_UNAVAILABLE
        )