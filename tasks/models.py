# tasks/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField()
    priority = models.CharField(max_length=10, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)  # New field to track completion
    created_at = models.DateTimeField(default=timezone.now)  # New field to track creation time
    updated_at = models.DateTimeField(auto_now=True)  # New field to track last update time
    reminder_time = models.DateTimeField(blank=True, null=True)  # New field for reminder time
    
    def __str__(self):
        return self.title


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)  # New field to track if the notification has been read
    created_at = models.DateTimeField(auto_now_add=True)  # New field to track when the notification was created

    def __str__(self):
        return f'Notification for {self.user.username} - {self.message}'