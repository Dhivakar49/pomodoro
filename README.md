# 🎯 FocusAI - Pomodoro Timer with AI-Powered Study Assistant

A modern, feature-rich Pomodoro timer application with AI-powered document analysis, task management, and productivity analytics.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🍅 Pomodoro Timer
- Customizable focus sessions (25/5/15 minutes)
- Visual progress ring with smooth animations
- Session tracking and statistics
- Task integration for focused work

### ✅ Task Management
- Create and organize tasks
- Set priorities (High/Medium/Low)
- Due date tracking
- Pomodoro count per task
- Progress visualization

### 📄 AI-Powered Document Analysis
- Upload PDF, DOC, DOCX, TXT files
- Automatic text extraction with OCR support
- AI-generated summaries (OpenAI/Hugging Face)
- Interactive quiz generation
- Document library management

### 📊 Analytics Dashboard
- Total sessions completed
- Focused time tracking
- Task completion statistics
- Visual productivity trends

### 🎨 Modern UI/UX
- Dark glassmorphic design
- Gradient accents and smooth animations
- Fully responsive (mobile-friendly)
- Professional typography

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip package manager
- (Optional) PostgreSQL for production

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/Dhivakar49/pomodoro.git
cd pomodoro
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

7. **Start development server**
```bash
python manage.py runserver
```

8. **Open in browser**
```
http://127.0.0.1:8000
```

## 🌐 Deploy to Render

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for complete deployment instructions.

**Quick Deploy:**
1. Create PostgreSQL database on Render
2. Create Web Service connected to this repo
3. Set environment variables (SECRET_KEY, DATABASE_URL, OPENAI_API_KEY)
4. Deploy! ✨

## 📁 Project Structure

```
pomodoro/
├── ai_engine/              # AI processing modules
│   ├── quiz_generator.py   # Quiz generation logic
│   ├── summarizer.py       # Text summarization
│   ├── text_extractor.py   # PDF/OCR extraction
│   └── prompts.py          # AI prompts
├── analytics/              # Analytics app
├── backend/                # Django settings
├── documents/              # Document management
├── frontend/               # Templates & static files
│   ├── static/
│   │   ├── css/           # Styles
│   │   └── js/            # JavaScript
│   └── templates/         # HTML templates
├── media/                  # User uploads
├── pomodoro/              # Pomodoro timer app
├── tasks/                 # Task management app
├── .env.example           # Environment template
├── .gitignore            # Git ignore rules
├── build.sh              # Render build script
├── manage.py             # Django management
├── Procfile              # Process file
├── render.yaml           # Render configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (False in production) | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Production |
| `OPENAI_API_KEY` | OpenAI API key | Optional* |
| `AI_PROVIDER` | AI provider (openai/huggingface) | Optional |
| `HF_API_KEY` | Hugging Face API key | Optional* |

*At least one AI provider key is needed for document analysis features

### Database

**Development:** SQLite (default)
**Production:** PostgreSQL (via DATABASE_URL)

## 🛠️ Technology Stack

**Backend:**
- Django 5.2
- Django REST Framework
- PostgreSQL / SQLite
- Gunicorn

**Frontend:**
- HTML5, CSS3, JavaScript
- Modern CSS (Glassmorphism)
- Vanilla JS (no frameworks)

**AI/ML:**
- OpenAI GPT API
- Hugging Face Transformers
- PyPDF2 (PDF processing)
- Pytesseract (OCR)

**Deployment:**
- Render (Platform)
- WhiteNoise (Static files)
- dj-database-url (Database config)

## 📸 Screenshots

### Timer Dashboard
Modern Pomodoro timer with task selection and progress tracking.

### Task Management
Organize tasks with priorities, due dates, and Pomodoro counts.

### Document Analysis
Upload documents and get AI-generated summaries and quizzes.

### Analytics
Track your productivity with detailed statistics.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Dhivakar**
- GitHub: [@Dhivakar49](https://github.com/Dhivakar49)

## 🙏 Acknowledgments

- Pomodoro Technique by Francesco Cirillo
- Design inspiration from modern productivity apps
- AI capabilities powered by OpenAI and Hugging Face

## 📞 Support

For issues and questions:
- Open an [Issue](https://github.com/Dhivakar49/pomodoro/issues)
- Check [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for deployment help

---

Made with ❤️ and ☕ by Dhivakar
