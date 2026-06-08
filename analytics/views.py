from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Count
from pomodoro.models import PomodoroSession
from tasks.models import Task

@api_view(['GET'])
def get_analytics(request):
    """
    Returns analytics data for the dashboard
    """
    total_sessions = PomodoroSession.objects.filter(completed=True).count()
    total_minutes = PomodoroSession.objects.filter(completed=True).aggregate(
        total=Sum('duration')
    )['total'] or 0
    tasks_completed = Task.objects.filter(completed=True).count()
    
    return Response({
        'total_sessions': total_sessions,
        'total_minutes': total_minutes,
        'tasks_completed': tasks_completed
    })
