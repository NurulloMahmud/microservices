# tasks/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from rest_framework import status


class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Requires JWT token

    def post(self, request):
        print(f"request: {request}")
        print(f"request.user: {request.user}")
        # Access the user_id from the custom SimpleUser object
        user_id = getattr(request.user, 'user_id', None)

        # Check if user_id is valid
        if not user_id:
            return Response({"detail": "User not found", "code": "user_not_found"}, status=401)

        # Proceed with task creation
        title = request.data.get('title')
        description = request.data.get('description')
        task = Task.objects.create(user_id=user_id, title=title, description=description)
        return Response({'task_id': task.id, 'title': task.title}, status=status.HTTP_201_CREATED)
