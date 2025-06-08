# tasks/views.py

from django.shortcuts import render, redirect
from .models import Task, Notification
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from datetime import timedelta, datetime
from django.utils import timezone
from django.contrib import messages

@login_required
def dashboard(request):
    filter_status = request.GET.get('filter', 'all')  # Get filter status from query parameters
    tasks = Task.objects.filter(user=request.user)

    if filter_status == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_status == 'pending':
        tasks = tasks.filter(completed=False)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    notifications = Notification.objects.filter(user=request.user, is_read=False)

    # Suggestion logic
    suggested_tasks = Task.objects.filter(user=request.user, completed=False).order_by('-priority', 'deadline')[:5] # suggest top 5 pending tasks
    
    context = {
        'tasks': tasks,
        'filter_status': filter_status,  # Pass the current filter status to the template
        'notifications': notifications,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': completion_rate,
        'suggested_tasks': suggested_tasks,  # Pass suggested tasks to the template
    }
    return render(request, 'tasks/dashboard.html', context)

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        deadline = request.POST['deadline']
        priority = request.POST['priority']
        task = Task(title=title, description=description, deadline=deadline, priority=priority, user=request.user)
        task.save()
        return redirect('tasks:dashboard')
    return render(request, 'tasks/add_task.html')

@login_required
def calendar_view(request):
    # You can pass any necessary data to the calendar here
    tasks = Task.objects.filter(user=request.user)
    events = []
    for task in tasks:
        events.append({
            'title': task.title,
            'start': task.deadline.isoformat(),
            'allDay': True,
            'id': task.id,
            'priority': task.priority,
            'description': task.description or '',
        })
    context = {
        'events': events,
    }
    return render(request, 'tasks/calendar.html', context)

@login_required
def calendar_events_json(request):
    # Return tasks as JSON for AJAX requests by calendar frontend
    tasks = Task.objects.filter(user=request.user)
    events = []
    for task in tasks:
        events.append({
            'title': task.title,
            'start': task.deadline.isoformat(),
            'allDay': True,
            'id': task.id,
            'description': task.description or '',
        })
    return JsonResponse(events, safe=False)

@login_required
def toggle_task_completion(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return JsonResponse({'completed': task.completed})

@login_required
def mark_notification_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success', 'message': 'Notification marked as read'})

@login_required
@csrf_exempt
def study_recommendations(request):
    recommendations = []
    user_input = ''
    if request.method == 'POST':
        user_input = request.POST.get('topic', '').strip().lower()
        # Basic static logic for demo purposes
        if 'math' in user_input:
            recommendations = [
                "Practice problem-solving daily with timed quizzes.",
                "Review foundational concepts before moving to complex topics.",
                "Use visual aids like graphs and charts to understand functions."
            ]
        elif 'physics' in user_input:
            recommendations = [
                "Focus on understanding core principles through experiments.",
                "Watch video lectures for difficult topics.",
                "Solve numerical problems regularly to build intuition."
            ]
        elif 'history' in user_input:
            recommendations = [
                "Create timelines to remember chronological events.",
                "Summarize key points in your own words.",
                "Discuss with peers to deepen understanding."
            ]
        else:
            recommendations = [
                "Set clear study goals and break them down into manageable parts.",
                "Use active recall and spaced repetition in your study sessions.",
                "Take regular breaks to maintain concentration."
            ]

    return render(request, 'tasks/study_recommendations.html', {
        'recommendations': recommendations,
        'user_input': user_input,
    })

@login_required
def voice_input(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        deadline = request.POST.get('deadline', '').strip()
        priority = request.POST.get('priority', 'Medium')

        if not title or not deadline:
            messages.error(request, 'Please provide at least a task title and deadline.')
            return render(request, 'tasks/voice_input.html', {'title': title, 'description': description, 'deadline': deadline, 'priority': priority})
        
        # Create task
        Task.objects.create(user=request.user, title=title, description=description, deadline=deadline, priority=priority)
        messages.success(request, f'Task "{title}" added successfully!')
        return redirect('tasks:dashboard')
    #Get request simply renders the page
    return render(request, 'tasks/voice_input.html')

@login_required
def upcoming_tasks_api(request):
    if request.method == 'GET':
        now = timezone.now()
        tasks = Task.objects.filter(deadline__gte=now).order_by('deadline')[:5]
        data = [
            {
                'id': task.id,
                'title': task.title,
                'deadline': task.deadline.strftime('%Y-%m-%d %H:%M'),
                'priority': task.priority,
            }
            for task in tasks
        ]
        return JsonResponse({'upcoming_tasks': data})
    else:
        return JsonResponse({'error': 'GET method required'}, status=400)