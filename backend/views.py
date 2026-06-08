from django.http import JsonResponse
from django.shortcuts import render

def dashboard_view(request):
    """Serve the dashboard page"""
    return render(request, 'dashboard.html')

def tasks_view(request):
    """Serve the tasks page"""
    return render(request, 'tasks.html')

def uploads_view(request):
    """Serve the uploads page"""
    return render(request, 'uploads.html')

def analytics_view(request):
    """Serve the analytics page"""
    return render(request, 'analytics.html')

def api_overview(request):
    """
    API Overview - List of available endpoints
    """
    endpoints = {
        "message": "Welcome to Focus AI Backend API",
        "available_endpoints": {
            "📝 Tasks API": {
                "List all tasks": "GET /api/tasks/",
                "Create task": "POST /api/tasks/create/",
                "List subjects": "GET /api/tasks/subjects/",
                "Create subject": "POST /api/tasks/subjects/create/"
            },
            "🍅 Pomodoro API": {
                "Start session": "POST /api/pomodoro/start/",
                "Complete session": "POST /api/pomodoro/complete/",
                "Save pomodoro": "POST /api/pomodoro/save/",
                "List subjects": "GET /api/pomodoro/subjects/",
                "Get stats": "GET /api/pomodoro/stats/"
            },
            "📄 Documents API": {
                "Upload file": "POST /api/documents/upload/",
            },
            "⚙️ Admin": {
                "Admin panel": "GET /admin/"
            }
        },
        "documentation": {
            "Base URL": "http://127.0.0.1:8000",
            "File uploads": "Send files as multipart/form-data with 'file' field",
        }
    }
    return JsonResponse(endpoints, json_dumps_params={'indent': 2})
