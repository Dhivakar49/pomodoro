from django.utils import timezone
from django.db.models import Sum, Count
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tasks.models import Subject
from .models import PomodoroSession

@csrf_exempt
@api_view(['POST'])
def start_session(request):
    subject_id = request.data.get('subject_id')

    if not subject_id:
        return Response({'error': 'subject_id is required'}, status=400)

    try:
        subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        return Response({'error': 'Invalid subject_id'}, status=400)

    session = PomodoroSession.objects.create(subject=subject, start_time=timezone.now())
    return Response({'message': 'Session started', 'id': session.id})

@csrf_exempt
@api_view(['POST'])
def complete_session(request):
    session_id = request.data.get('session_id')
    
    try:
        session = PomodoroSession.objects.get(id=session_id)
    except PomodoroSession.DoesNotExist:
        return Response({"error": "Session not found"}, status=404)

    session.end_time = timezone.now()
    session.completed = True
    session.save()

    return Response({
        "message": "Session completed",
        "id": session.id,
        "start_time": session.start_time,
        "end_time": session.end_time
    })

@api_view(['GET'])
def list_subjects(request):
    subjects = Subject.objects.all().values('id', 'name')
    return Response(list(subjects))

@csrf_exempt
@api_view(['POST'])
def save_pomodoro(request):
    try:
        subject_id = request.data.get("subject_id")
        duration = request.data.get("duration", 25)
        start_time = request.data.get("start_time")
        end_time = request.data.get("end_time")

        # If no subject provided, create or get a default one
        if not subject_id:
            subject, created = Subject.objects.get_or_create(name='General')
        else:
            try:
                subject = Subject.objects.get(id=subject_id)
            except Subject.DoesNotExist:
                subject, created = Subject.objects.get_or_create(name='General')

        session = PomodoroSession.objects.create(
            subject=subject,
            duration=duration,
            start_time=start_time if start_time else timezone.now(),
            end_time=end_time if end_time else timezone.now(),
            completed=True
        )

        return Response({
            "message": "Pomodoro saved",
            "session_id": session.id
        }, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['GET'])
def get_stats(request):
    stats = PomodoroSession.objects.values('subject__name').annotate(
        total_minutes=Sum('duration'),
        sessions=Count('id')
    )

    total_time = PomodoroSession.objects.aggregate(Sum('duration'))

    return Response({
        "total_minutes": total_time['duration__sum'],
        "subjects": list(stats)
    })