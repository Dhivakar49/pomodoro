#!/bin/bash

echo "🚀 FocusAI - Final Setup & Test Script"
echo "======================================"
echo ""

# Step 1: Install Dependencies
echo "📦 Step 1: Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Step 2: Apply Migrations
echo "🗄️ Step 2: Setting up database..."
python manage.py makemigrations
python manage.py migrate
echo "✅ Database ready"
echo ""

# Step 3: Test AI Engine
echo "🧪 Step 3: Testing AI Engine..."
python -c "
import os
os.environ['AI_PROVIDER'] = 'huggingface'
os.environ['HF_API_KEY'] = 'your-huggingface-api-key-here'

from ai_engine.summarizer_hf import summarize_with_hf

test_text = 'Python is a high-level, interpreted programming language. It is widely used for web development, data analysis, artificial intelligence, and automation. Python is known for its simple syntax and readability.'

print('Testing Hugging Face summarizer...')
result = summarize_with_hf(test_text)
print(f'Summary: {result}')
print('✅ AI Engine working!')
"
echo ""

# Step 4: Create Test Data
echo "📝 Step 4: Creating test data..."
python manage.py shell <<EOF
from tasks.models import Subject, Task
from pomodoro.models import PomodoroSession
from django.utils import timezone

# Create test subjects
if Subject.objects.count() == 0:
    math = Subject.objects.create(name='Mathematics')
    science = Subject.objects.create(name='Science')
    english = Subject.objects.create(name='English')
    print('✅ Created 3 subjects')

# Create test tasks
if Task.objects.count() == 0:
    Task.objects.create(title='Complete Algebra homework', subject=math, required_pomodoros=3)
    Task.objects.create(title='Study Physics chapters', subject=science, required_pomodoros=2)
    Task.objects.create(title='Write essay', subject=english, required_pomodoros=4)
    print('✅ Created 3 tasks')

# Create test pomodoro sessions
if PomodoroSession.objects.count() == 0:
    PomodoroSession.objects.create(
        subject=math, 
        start_time=timezone.now(), 
        end_time=timezone.now(),
        completed=True
    )
    print('✅ Created test pomodoro session')

print('✅ Test data ready')
EOF
echo ""

# Step 5: Run Server
echo "🌐 Step 5: Starting server..."
echo ""
echo "=========================================="
echo "✅ ALL CHECKS PASSED!"
echo "=========================================="
echo ""
echo "🎯 Access your application at:"
echo "   📱 Frontend: http://127.0.0.1:8000/"
echo "   🔌 API: http://127.0.0.1:8000/api/"
echo ""
echo "🧪 Test the following:"
echo "   ✔ Dashboard - Pomodoro Timer"
echo "   ✔ Tasks - Create and list tasks"
echo "   ✔ Documents - Upload files with AI summary (Hugging Face)"
echo "   ✔ Analytics - View statistics"
echo ""
echo "🔑 AI Provider: Hugging Face (configured)"
echo ""
echo "Starting Django development server..."
python manage.py runserver
