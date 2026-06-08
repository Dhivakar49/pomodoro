from django.urls import path
from .views import create_subject, list_subjects, create_task, list_tasks, tasks_handler, task_detail

urlpatterns = [
    path('subjects/create/', create_subject),
    path('subjects/', list_subjects),
    path('create/', create_task),
    path('', tasks_handler),  # Handle both GET and POST
    path('<int:task_id>/', task_detail),  # Handle PATCH and DELETE
]
