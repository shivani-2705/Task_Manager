from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.utils.timezone import now
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib import messages
import re
from .models import Task, User


#  AUTHENTICATION VIEWS (WEB ONLY)

def register_view(request):
    """
    Renders the user registration page and handles user signup.
    Includes validation for email, password, and mobile number.
    """
    if request.method == "POST":
        username = request.POST['username'].strip()
        email = request.POST['email'].strip().lower()  # Convert email to lowercase
        password = request.POST['password']
        retype_password = request.POST['retype_password']
        mobile = request.POST['mobile'].strip()

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return render(request, "register.html", {"error": "Invalid email format. Use abc@gmail.com"})

        # Validate password strength
        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return render(request, "register.html", {"error": "Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and a special character."})

        # Check password confirmation
        if password != retype_password:
            return render(request, "register.html", {"error": "Passwords do not match"})

        # Validate mobile number (10 digits only)
        if not re.match(r'^\d{10}$', mobile):
            return render(request, "register.html", {"error": "Mobile number must be exactly 10 digits."})

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email already exists"})

        # Save user after all validations pass
        user = User(username=username, email=email, mobile=mobile)
        user.set_password(password)  # Hash password before saving
        user.save()

        return redirect('login')  # Redirect to login after successful registration

    return render(request, "register.html")


def login_view(request):
    """
    Renders the login page and authenticates the user.
    Redirects to the task list page after successful login.
    """
    if request.method == "POST":
        email = request.POST['email'].strip().lower()
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('task_list')  # Redirect to the task list page
        else:
            return render(request, "login.html", {"error": "Invalid email or password"})

    return render(request, "login.html")


@login_required(login_url='login')
def logout_view(request):
    """
    Logs out the user and redirects them to the login page.
    """
    logout(request)
    return redirect('login')


 # TASK MANAGEMENT VIEWS (WEB ONLY)


@login_required(login_url='login')
def task_list_view(request):
    """
    Displays tasks in two categories:
    - Tasks Created by the User
    - Tasks Assigned to the User (including self-assigned tasks)
    """
    created_tasks = Task.objects.filter(created_by=request.user)
    assigned_tasks = Task.objects.filter(assigned_users=request.user)

    return render(request, "task_list.html", {
        "created_tasks": created_tasks,
        "assigned_tasks": assigned_tasks,  
    })


@login_required(login_url='login')
def task_create_view(request):
    """
    Renders the task creation page and handles new task creation.
    The creator is NOT automatically assigned unless selected.
    """
    TASK_TYPE_CHOICES = ['Bug', 'Feature', 'Improvement', 'Research']

    if request.method == "POST":
        name = request.POST['name'].strip()
        description = request.POST['description'].strip()
        task_type = request.POST.get('task_type', '')
        assigned_user_ids = request.POST.getlist('assigned_users')

        # Validate task name
        if len(name) < 3 or len(name) > 255:
            return render(request, "task_create.html", {"error": "Task name must be between 3 and 255 characters."})

        # Validate task type
        if task_type not in TASK_TYPE_CHOICES:
            return render(request, "task_create.html", {"error": "Invalid task type"})

        # Prevent duplicate tasks
        if Task.objects.filter(name=name, description=description).exists():
            return render(request, "task_create.html", {"error": "A task with the same name and description already exists."})

        #  Create task (without assigning creator by default)
        task = Task.objects.create(
            name=name,
            description=description,
            task_type=task_type,
            created_by=request.user  # Creator is stored but NOT assigned automatically
        )

        #  Assign selected users (including creator if they chose themselves)
        if assigned_user_ids:
            assigned_users = User.objects.filter(id__in=assigned_user_ids)
            task.assigned_users.set(assigned_users)

        return redirect('task_list')

    #  Show all users including the creator as an option to assign
    users = User.objects.all()
    return render(request, "task_create.html", {"task_types": TASK_TYPE_CHOICES, "users": users})


@login_required(login_url='login')
def assign_users_view(request, task_id):
    """
    Allows assigning users to an existing task.
    The user cannot assign themselves if already assigned.
    """
    task = Task.objects.get(id=task_id)

    if request.method == "POST":
        assigned_user_ids = request.POST.getlist('assigned_users')
        users_to_add = User.objects.filter(id__in=assigned_user_ids).exclude(id__in=task.assigned_users.all())

        if users_to_add.exists():
            task.assigned_users.add(*users_to_add)

        return redirect('task_list')

    # Exclude already assigned users (including the current user if assigned)
    available_users = User.objects.exclude(id__in=task.assigned_users.values_list('id', flat=True))

    return render(request, "assign_users.html", {"task": task, "users": available_users})


@login_required(login_url='login')
def update_task_status(request, task_id):
    """
    Updates the status of a task.
    - Allows users to change the task status.
    - If the status is set to 'Completed', updates `completed_at` timestamp.
    """
    task = get_object_or_404(Task, id=task_id)

    # Ensure only assigned users can update the task
    if request.user not in task.assigned_users.all():
        messages.error(request, "You are not assigned to this task.")
        return redirect('task_list')

    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status in ["Pending", "In Progress", "Completed"]:
            task.status = new_status
            if new_status == "Completed":
                task.completed_at = now()  # Set completed time when task is done
            task.save()
            messages.success(request, "Task status updated successfully.")
        else:
            messages.error(request, "Invalid status selected.")

    return redirect('task_list')


#  TASK MANAGEMENT API VIEWS

@csrf_exempt  # Allow requests from any source (disable CSRF for simplicity)
def api_create_task(request):
    """
    API to create a new task.
    Allows anyone to create a task without authentication.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        task_type = data.get('task_type', '')
        assigned_user_ids = data.get('assigned_users', [])  # Expecting a list

        # Validate task name & description
        if not name or len(name) < 3:
            return JsonResponse({"error": "Task name must be at least 3 characters long."}, status=400)

        if not description:
            return JsonResponse({"error": "Task description is required."}, status=400)

        # Validate task type
        TASK_TYPE_CHOICES = ['Bug', 'Feature', 'Improvement', 'Research']
        if task_type not in TASK_TYPE_CHOICES:
            return JsonResponse({"error": "Invalid task type."}, status=400)

        # Create the task
        task = Task.objects.create(
            name=name,
            description=description,
            task_type=task_type
        )

        #  Assign users (if selected)
        if assigned_user_ids:
            assigned_users = User.objects.filter(id__in=assigned_user_ids)
            task.assigned_users.set(assigned_users)

        return JsonResponse({
            "message": "Task created successfully",
            "task_id": task.id,
            "task_name": task.name,
            "assigned_users": list(task.assigned_users.values('id', 'username')),
        }, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def api_assign_users(request, task_id):
    """
    API to assign users to an existing task.
    - Prevents assigning users if the task is completed.
    - Prevents duplicate assignments.
    - Does not require authentication.
    """
    task = Task.objects.filter(id=task_id).first()

    if not task:
        return JsonResponse({"error": "Task not found"}, status=404)

    if task.status == "Completed":
        return JsonResponse({"error": "Cannot assign users to a completed task."}, status=400)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        assigned_user_ids = data.get('assigned_users', [])  # Expecting a list

        # Get users that are not already assigned
        users_to_add = User.objects.filter(id__in=assigned_user_ids).exclude(id__in=task.assigned_users.all())

        if users_to_add.exists():
            task.assigned_users.add(*users_to_add)
            return JsonResponse({"message": "Users assigned successfully."}, status=200)
        
        return JsonResponse({"error": "No new users to assign."}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def api_list_tasks(request):
    """
    API to retrieve all tasks assigned to a specific user.
    - Requires 'email' or 'user_id' in the request.
    - Does not require authentication.
    """
    if request.method == "GET":
        user_email = request.GET.get('email', '').strip().lower()
        user_id = request.GET.get('user_id', '').strip()

        # Find user by email or ID
        user = None
        if user_email:
            user = User.objects.filter(email=user_email).first()
        elif user_id.isdigit():
            user = User.objects.filter(id=int(user_id)).first()

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        # Fetch tasks assigned to the user
        tasks = Task.objects.filter(assigned_users=user).values(
            'id', 'name', 'description', 'task_type', 'status', 'created_at', 'completed_at'
        )

        return JsonResponse({"tasks": list(tasks)}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)
