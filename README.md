# FocusAI - Pomodoro Timer with AI-Powered Study Assistant

A comprehensive study management system combining the Pomodoro Technique with AI-powered document analysis.

## 🎯 Features

- ⏱️ **Pomodoro Timer** - Focused study sessions
- 📝 **Task Management** - Organize your study tasks
- 🤖 **AI Document Analysis** - Upload PDFs and get AI summaries
- 📊 **Analytics Dashboard** - Track your productivity
- 🎓 **Quiz Generation** - AI-generated quizzes from your documents

## 🏗️ Architecture

```
✔ Frontend talks ONLY via APIs
✔ Backend stores data
✔ AI logic fully separated
✔ Fallback works without API key
✔ Everything testable
```

### Project Structure

```
pomodoro-main/
├── backend/              # Django settings & main URLs
├── frontend/             # HTML templates & static files
│   ├── templates/        # HTML pages
│   └── static/          # CSS & JavaScript
├── ai_engine/           # AI processing (separated)
│   ├── text_extractor.py
│   ├── summarizer.py
│   ├── quiz_generator.py
│   └── prompts.py
├── pomodoro/            # Timer sessions
├── tasks/               # Task management
├── documents/           # File uploads
└── analytics/           # Statistics
```

## 🚀 Installation

### Prerequisites
- Python 3.9+
- PostgreSQL (or use SQLite for development)
- Tesseract OCR (for image text extraction)

### Setup Steps

1. **Clone the repository**
```bash
cd /home/premkumar/Downloads/pomodoro-main
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here  # Optional
SECRET_KEY=your_django_secret_key
DEBUG=True
```

5. **Database setup**
```bash
# For PostgreSQL (update settings.py with your credentials)
# Or switch to SQLite for development:
# In backend/settings.py, change DATABASES to:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run the server**
```bash
python manage.py runserver
```

8. **Access the application**
- Dashboard: http://127.0.0.1:8000/
- Tasks: http://127.0.0.1:8000/tasks/
- Documents: http://127.0.0.1:8000/uploads/
- Analytics: http://127.0.0.1:8000/analytics/
- Admin: http://127.0.0.1:8000/admin/

## 🔌 API Endpoints

### Tasks API
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/create/` - Create task
- `GET /api/tasks/subjects/` - List subjects
- `POST /api/tasks/subjects/create/` - Create subject

### Pomodoro API
- `POST /api/pomodoro/start/` - Start timer session
- `POST /api/pomodoro/complete/` - Complete session
- `POST /api/pomodoro/save/` - Save pomodoro
- `GET /api/pomodoro/stats/` - Get statistics

### Documents API
- `POST /api/documents/` - Upload document (returns AI summary)
- `GET /api/documents/` - List uploaded documents
- `DELETE /api/documents/{id}/` - Delete document

### Analytics API
- `GET /api/analytics/` - Get productivity statistics

## 🤖 AI Features

### Text Extraction
Supports PDF and image files using PyPDF2 and Tesseract OCR.

### AI Summarization
- Uses OpenAI GPT-3.5-turbo
- Falls back to mock summary if API key not configured
- No errors if OpenAI is unavailable

### Quiz Generation
AI-generated multiple-choice questions from uploaded content.

## 🧪 Testing

The application is fully testable with separated concerns:
- Frontend uses only API calls (fetch)
- Backend handles all data storage
- AI engine is modular and mockable

## 📝 Development Notes

- **Database**: PostgreSQL configured, can switch to SQLite for development
- **CSRF**: Disabled for API endpoints using @api_view decorator
- **File Uploads**: Stored in `media/documents/`
- **Static Files**: Located in `frontend/static/`
- **Templates**: Located in `frontend/templates/`

## 🎨 Frontend Technology

- Pure HTML/CSS/JavaScript
- No framework dependencies
- Fetch API for all backend communication
- Modern gradient UI design

## 🔐 Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Configure ALLOWED_HOSTS
- Use environment variables for sensitive data
- Enable HTTPS in production

## 📦 Production Deployment

1. Set environment variables
2. Configure production database
3. Collect static files: `python manage.py collectstatic`
4. Use gunicorn or uwsgi
5. Set up nginx as reverse proxy
6. Enable HTTPS

## 🤝 Contributing

This is an educational project. Feel free to extend and improve!

## 📄 License

MIT License - Feel free to use for learning and development.
# hackathon1
# hackathon1
