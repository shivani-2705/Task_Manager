from django.contrib import admin
from .models import User, Task

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'mobile', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'mobile')
    list_filter = ('is_staff', 'is_active')
    ordering = ('id',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'task_type', 'status', 'created_by', 'created_at', 'completed_at')
    search_fields = ('name', 'description', 'created_by__email')
    list_filter = ('status', 'task_type', 'created_at')
    ordering = ('-created_at',)
    filter_horizontal = ('assigned_users',)  # Enables a better UI for ManyToMany fields

