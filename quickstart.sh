#!/bin/bash
# Quick Start Script for FocusAI

echo "🚀 FocusAI - Quick Start"
echo "========================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo "🗄️ Setting up database..."
python3 manage.py makemigrations
python3 manage.py migrate

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Create a superuser to access admin panel:"
echo "   python3 manage.py createsuperuser"
echo ""
echo "🚀 Start the server:"
echo "   python3 manage.py runserver"
echo ""
echo "🌐 Access the application:"
echo "   Dashboard:  http://127.0.0.1:8000/"
echo "   Tasks:      http://127.0.0.1:8000/tasks/"
echo "   Documents:  http://127.0.0.1:8000/uploads/"
echo "   Analytics:  http://127.0.0.1:8000/analytics/"
echo "   Admin:      http://127.0.0.1:8000/admin/"
echo ""
