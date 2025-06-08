from django.urls import path
from .views import dashboard, add_task, calendar_view,\
      calendar_events_json, toggle_task_completion,\
          mark_notification_read, study_recommendations, voice_input, upcoming_tasks_api

app_name = 'tasks'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('add/', add_task, name='add_task'),
    path('calendar/', calendar_view, name='calendar'),
    path('calendar/events/', calendar_events_json, name='calendar_events_json'),
    path('toggle_task_completion/<int:task_id>/', toggle_task_completion, name='toggle_task_completion'),  # New route
    path('mark_notification_read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),
    path('study_recommendations/', study_recommendations, name='study_recommendations'),
    path('voice_input/', voice_input, name='voice_input'),
    path('api/upcoming_tasks/', upcoming_tasks_api, name='upcoming_tasks_api'),
    

]
