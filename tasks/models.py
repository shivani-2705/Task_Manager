from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, validate_email
from django.utils.timezone import now


#  USER MODEL

class User(AbstractUser):
    """
    Custom User model with email as the primary identifier.
    Enforces unique email and valid mobile number.
    """
    email = models.EmailField(unique=True, validators=[validate_email])  
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[
            RegexValidator(regex=r'^[a-zA-Z0-9_]+$', message="Username can only contain letters, numbers, and underscores."),
        ]
    )
    mobile = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message="Mobile number must be exactly 10 digits.")],
        unique=True,
        default="0000000000" 
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# TASK MODEL


class Task(models.Model):
    """
    Represents a task in the system.
    A task can be assigned to multiple users, and a user can have multiple tasks.
    """
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ]

    TASK_TYPE_CHOICES = [
        ('Bug', 'Bug'),
        ('Feature', 'Feature'),
        ('Improvement', 'Improvement'),
        ('Research', 'Research'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default='Feature', blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks" , null=True)  # ✅ Track creator

    assigned_users = models.ManyToManyField(User, related_name='tasks', blank=True)

    class Meta:
        ordering = ['-created_at']  # Show newest tasks first

    def save(self, *args, **kwargs):
        """
        Automatically set `completed_at` when status is changed to 'Completed'.
        """
        if self.status == 'Completed' and not self.completed_at:
            self.completed_at = now()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Ensure all Many-to-Many relations are removed before deleting the task.
        """
        self.assigned_users.clear()  #  Remove all user-task relationships
        super().delete(*args, **kwargs)  # Now delete task safely

    def __str__(self):
        return f"{self.name} - {self.status}"
