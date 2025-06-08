from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Task, Notification
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send notifications for upcoming tasks'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        upcoming_tasks = Task.objects.filter(reminder_time_gte=now, reminder_time_lt=now + timedelta(hours=1))
        
        for task in upcoming_tasks:
            message = f"Reminder: Task '{task.title}' is due soon!"
            Notification.objects.create(
                user=task.user,
                task=task,
                message=message
            )
            self.stdout.write(self.style.SUCCESS(f'Notification sent for task: {task.title}'))
        self.stdout.write(self.style.SUCCESS('All notifications sent successfully.'))