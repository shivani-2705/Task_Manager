"""
This file contains serializer classes for converting Django model instances
into JSON for API responses and handling API requests.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

# ==============================
# 🚀 USER SERIALIZER
# ==============================

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Excludes sensitive fields like password in API responses.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile']
        extra_kwargs = {
            'password': {'write_only': True},  # ✅ Prevent password from being exposed
        }

# ==============================
# 🚀 TASK SERIALIZER
# ==============================

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    Allows assigning users by IDs and ensures `completed_at` is read-only.
    """
    assigned_users = UserSerializer(many=True, read_only=True)  # ✅ Show assigned users in response
    assigned_users_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigned_users', many=True, write_only=True, required=False
    )  # ✅ Accept user IDs in request

    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'created_at', 'completed_at',
            'status', 'task_type', 'assigned_users', 'assigned_users_ids'
        ]
        read_only_fields = ['completed_at']  # ✅ Prevent users from manually setting completed_at
