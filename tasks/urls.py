from django.urls import path
from .views import (
    register_view, login_view, logout_view,
    task_list_view, task_create_view, assign_users_view,
    update_task_status, api_create_task, api_assign_users, api_list_tasks
)

urlpatterns = [
    # ✅ Authentication Routes
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # ✅ Task Management (Web UI)
    path('tasks/', task_list_view, name='task_list'),
    path('tasks/create/', task_create_view, name='task_create'),
    path('tasks/<int:task_id>/assign/', assign_users_view, name='assign_users'), 
    path('tasks/update_status/<int:task_id>/', update_task_status, name='update_task_status'),

    # ✅ Task Management (API)
    path('api/tasks/create/', api_create_task, name='api_create_task'),
    path('api/tasks/', api_list_tasks, name='api_list_tasks'),  
    path('api/tasks/<int:task_id>/assign/', api_assign_users, name='api_assign_users'),  
]
