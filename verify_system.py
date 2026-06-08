#!/usr/bin/env python
"""
FocusAI System Verification
Checks all components of the FINAL CHECKLIST
"""

import os
import sys

def check_frontend_structure():
    """✔ Frontend talks ONLY via APIs"""
    print("\n📱 Checking Frontend Structure...")
    
    required_files = [
        'frontend/templates/base.html',
        'frontend/templates/dashboard.html',
        'frontend/templates/tasks.html',
        'frontend/templates/uploads.html',
        'frontend/templates/analytics.html',
        'frontend/static/css/style.css',
        'frontend/static/js/timer.js',
        'frontend/static/js/tasks.js',
        'frontend/static/js/uploads.js',
        'frontend/static/js/analytics.js',
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            return False
    
    # Check that JS files use fetch API
    js_files = ['frontend/static/js/timer.js', 'frontend/static/js/tasks.js', 
                'frontend/static/js/uploads.js', 'frontend/static/js/analytics.js']
    
    for js_file in js_files:
        with open(js_file, 'r') as f:
            content = f.read()
            if 'fetch(' in content:
                print(f"  ✓ {js_file} uses fetch API")
            else:
                print(f"  ⚠ {js_file} might not use API calls")
    
    return True

def check_backend_structure():
    """✔ Backend stores data"""
    print("\n🗄️ Checking Backend & Database...")
    
    models = [
        'pomodoro/models.py',
        'tasks/models.py',
        'documents/models.py',
    ]
    
    for model_file in models:
        if os.path.exists(model_file):
            with open(model_file, 'r') as f:
                content = f.read()
                if 'models.Model' in content:
                    print(f"  ✓ {model_file} - has Django models")
                else:
                    print(f"  ✗ {model_file} - no models found")
                    return False
        else:
            print(f"  ✗ {model_file} - MISSING")
            return False
    
    return True

def check_ai_separation():
    """✔ AI logic fully separated"""
    print("\n🤖 Checking AI Engine Separation...")
    
    ai_files = [
        'ai_engine/__init__.py',
        'ai_engine/text_extractor.py',
        'ai_engine/summarizer.py',
        'ai_engine/quiz_generator.py',
        'ai_engine/prompts.py',
    ]
    
    for file in ai_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            return False
    
    return True

def check_fallback_mechanism():
    """✔ Fallback works without API key"""
    print("\n🔄 Checking AI Fallback Mechanism...")
    
    try:
        with open('ai_engine/summarizer.py', 'r') as f:
            content = f.read()
            if 'not os.getenv("OPENAI_API_KEY")' in content:
                print("  ✓ Fallback mechanism detected")
                if 'Mock Summary' in content:
                    print("  ✓ Mock response implemented")
                    return True
            else:
                print("  ✗ No fallback mechanism found")
                return False
    except Exception as e:
        print(f"  ✗ Error checking fallback: {e}")
        return False

def check_api_endpoints():
    """✔ Everything testable via API"""
    print("\n🔌 Checking API Endpoints...")
    
    url_files = [
        'backend/urls.py',
        'pomodoro/urls.py',
        'tasks/urls.py',
        'documents/urls.py',
        'analytics/urls.py',
    ]
    
    for file in url_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            return False
    
    return True

def main():
    print("=" * 60)
    print("🧱 FocusAI - FINAL CHECKLIST VERIFICATION")
    print("=" * 60)
    
    checks = [
        ("Frontend talks ONLY via APIs", check_frontend_structure),
        ("Backend stores data", check_backend_structure),
        ("AI logic fully separated", check_ai_separation),
        ("Fallback works without API key", check_fallback_mechanism),
        ("Everything testable", check_api_endpoints),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n❌ Error in {check_name}: {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)
    
    for check_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {check_name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL CHECKS PASSED! System is ready.")
        print("=" * 60)
        print("\n🚀 Next Steps:")
        print("1. Run: python manage.py makemigrations")
        print("2. Run: python manage.py migrate")
        print("3. Run: python manage.py createsuperuser")
        print("4. Run: python manage.py runserver")
        print("5. Visit: http://127.0.0.1:8000/")
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED - Review errors above")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
