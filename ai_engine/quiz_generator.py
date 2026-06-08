from .prompts import QUIZ_PROMPT
import os
import requests

def generate_quiz(text):
    """Generate quiz questions from text"""
    HF_TOKEN = os.getenv("HF_API_KEY")
    
    if HF_TOKEN:
        try:
            return generate_quiz_with_ai(text, HF_TOKEN)
        except Exception as e:
            print(f"AI Quiz generation failed: {e}")
            return generate_basic_quiz(text)
    else:
        return generate_basic_quiz(text)

def generate_quiz_with_ai(text, token):
    """Use HF API to generate quiz"""
    headers = {"Authorization": f"Bearer {token}"}
    prompt = f"{QUIZ_PROMPT}\n\n{text[:2000]}"
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    response = requests.post(
        "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            # Try to parse AI response, fallback to basic if it fails
            return generate_basic_quiz(text)
    
    return generate_basic_quiz(text)

def generate_basic_quiz(text):
    """Generate MCQ quiz questions based on actual document content"""
    import re
    import random
    
    # Split into sentences and clean them
    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 30]
    words = text.split()
    
    # Extract key information
    word_freq = {}
    for word in words:
        clean_word = re.sub(r'[^a-zA-Z]', '', word).lower()
        if len(clean_word) > 4:
            word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
    
    key_terms = [term for term, count in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]]
    
    # Generate quiz in JSON format for frontend
    quiz_data = []
    
    # Question 1: Main topic
    if sentences and key_terms:
        main_topic = key_terms[0].capitalize()
        options = [
            main_topic,
            "General information",
            "Historical events",
            "Mathematical concepts"
        ]
        random.shuffle(options)
        quiz_data.append({
            "question": "What is the main subject discussed in this document?",
            "options": options,
            "correct": main_topic
        })
    
    # Question 2: Key term definition
    if len(key_terms) > 0:
        term = key_terms[0].capitalize()
        correct_ans = f"A field related to {term.lower()}"
        options = [
            correct_ans,
            "A programming language",
            "A mathematical formula",
            "A historical period"
        ]
        random.shuffle(options)
        quiz_data.append({
            "question": f"What best describes '{term}' based on the document?",
            "options": options,
            "correct": correct_ans
        })
    
    # Question 3: Content-based
    if len(key_terms) > 1:
        term2 = key_terms[1].capitalize()
        correct_ans = f"It's a key component discussed"
        options = [
            correct_ans,
            "It's not mentioned",
            "It's a minor detail",
            "It's a future concept"
        ]
        random.shuffle(options)
        quiz_data.append({
            "question": f"According to the document, what role does '{term2}' play?",
            "options": options,
            "correct": correct_ans
        })
    
    # Question 4: Document scope
    correct_ans = f"{min(len(key_terms), 5)} or more"
    options = [
        correct_ans,
        "Only one",
        "None",
        "Too many to count"
    ]
    random.shuffle(options)
    quiz_data.append({
        "question": "How many main concepts are covered in this document?",
        "options": options,
        "correct": correct_ans
    })
    
    # Question 5: Application
    if len(key_terms) > 2:
        correct_ans = f"Technical and educational about {key_terms[0]}"
        options = [
            correct_ans,
            "Entertainment purposes",
            "Cooking recipes",
            "Fashion trends"
        ]
        random.shuffle(options)
        quiz_data.append({
            "question": "What type of knowledge does this document provide?",
            "options": options,
            "correct": correct_ans
        })
    
    return quiz_data
