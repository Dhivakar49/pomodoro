from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task, Subject

@csrf_exempt
@api_view(['POST'])
def create_subject(request):
    name = request.data.get('name')
    subject = Subject.objects.create(name=name)
    return Response({'message': 'Subject created', 'id': subject.id})

@api_view(['GET'])
def list_subjects(request):
    subjects = Subject.objects.all().values()
    return Response(list(subjects))

@csrf_exempt
@api_view(['POST'])
def create_task(request):
    title = request.data.get('title')
    subject_id = request.data.get('subject_id')
    required = request.data.get('required_pomodoros', 1)

    subject = Subject.objects.get(id=subject_id)
    task = Task.objects.create(title=title, subject=subject, required_pomodoros=required)
    return Response({'message': 'Task created', 'id': task.id})

@api_view(['GET'])
def list_tasks(request):
    tasks = Task.objects.all().values()
    return Response(list(tasks))

@csrf_exempt
@api_view(['GET', 'POST'])
def tasks_handler(request):
    """Handle both GET and POST requests for tasks"""
    if request.method == 'GET':
        tasks = Task.objects.all().values('id', 'title', 'completed', 'required_pomodoros', 'completed_pomodoros', 'subject_id', 'priority', 'due_date')
        return Response(list(tasks))
    elif request.method == 'POST':
        title = request.data.get('title')
        subject_id = request.data.get('subject_id')
        required = request.data.get('required_pomodoros', 1)
        priority = request.data.get('priority', 'medium')
        due_date = request.data.get('due_date', None)

        if not title:
            return Response({'error': 'Title is required'}, status=400)
        
        # Create subject if not provided
        if not subject_id:
            subject = Subject.objects.create(name='General')
            subject_id = subject.id
        else:
            try:
                subject = Subject.objects.get(id=subject_id)
            except Subject.DoesNotExist:
                return Response({'error': 'Subject not found'}, status=404)
        
        task = Task.objects.create(
            title=title,
            subject=subject,
            required_pomodoros=required,
            priority=priority,
            due_date=due_date if due_date else None
        )
        return Response({
            'message': 'Task created',
            'id': task.id,
            'title': task.title,
            'completed': task.completed,
            'required_pomodoros': task.required_pomodoros,
            'completed_pomodoros': task.completed_pomodoros,
            'priority': task.priority,
            'due_date': task.due_date
        })


@csrf_exempt
@api_view(['PATCH', 'DELETE'])
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=404)
    
    if request.method == 'PATCH':
        if 'completed' in request.data:
            task.completed = request.data['completed']
        if 'title' in request.data:
            task.title = request.data['title']
        if 'required_pomodoros' in request.data:
            task.required_pomodoros = request.data['required_pomodoros']
        if 'completed_pomodoros' in request.data:
            task.completed_pomodoros = request.data['completed_pomodoros']
        if 'priority' in request.data:
            task.priority = request.data['priority']
        if 'due_date' in request.data:
            task.due_date = request.data['due_date']
        task.save()
        return Response({
            'message': 'Task updated',
            'id': task.id,
            'title': task.title,
            'completed': task.completed,
            'required_pomodoros': task.required_pomodoros,
            'completed_pomodoros': task.completed_pomodoros,
            'priority': task.priority,
            'due_date': task.due_date
        })
    
    elif request.method == 'DELETE':
        task.delete()
        return Response({'message': 'Task deleted'}, status=200)
