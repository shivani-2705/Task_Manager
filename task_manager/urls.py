"""
Main URL routing for the Task Management Project.
Handles admin, authentication, and task management.
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# ✅ Redirect root URL to login if user is not authenticated
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('task_list')  # Redirect logged-in users to tasks
    return redirect('login')  # Redirect non-logged-in users to login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home_redirect'),  # ✅ Redirect to login or task list
    path('web/', include('tasks.urls')),  # ✅ Use '/web/' for all pages
    
]
