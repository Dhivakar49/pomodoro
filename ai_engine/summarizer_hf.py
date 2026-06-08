import os
import requests
from .prompts import SUMMARY_PROMPT

HF_TOKEN = os.getenv("HF_API_KEY")
# Using a more reliable model that supports both summarization and text generation
MODEL = "mistralai/Mistral-7B-Instruct-v0.1"

def summarize_with_hf(text):
    """Hugging Face alternative for text summarization"""
    if not HF_TOKEN:
        return generate_basic_summary(text)

    try:
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        # Create a prompt for the model
        prompt = f"{SUMMARY_PROMPT}\n\n{text[:4000]}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
                "return_full_text": False
            }
        }

        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL}",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", generate_basic_summary(text))
            return generate_basic_summary(text)
        else:
            print(f"HF API Error: {response.status_code}")
            return generate_basic_summary(text)
    except Exception as e:
        print(f"Error with Hugging Face: {str(e)}")
        return generate_basic_summary(text)

def generate_basic_summary(text):
    """Generate a comprehensive summary with key points and Q&A"""
    import re
    
    # Split into sentences
    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
    
    # Extract key information
    words = text.split()
    word_freq = {}
    for word in words:
        clean_word = re.sub(r'[^a-zA-Z]', '', word).lower()
        if len(clean_word) > 4:
            word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
    
    key_terms = [term for term, count in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:8]]
    
    # Build summary
    summary = "📝 SUMMARY\n\n"
    
    # Add main content (first 3-4 sentences)
    main_content = '. '.join(sentences[:4]) + '.'
    summary += f"{main_content}\n\n"
    
    # Add key points
    if key_terms:
        summary += "Key Topics Covered:\n"
        for i, term in enumerate(key_terms[:5], 1):
            summary += f"• {term.capitalize()}\n"
        summary += "\n"
    
    # Add Q&A section
    summary += "\n"
    
    if len(key_terms) > 0:
        summary += f"Q1: What is the main topic of this document?\n"
        summary += f"A1: This document primarily discusses {key_terms[0]} and related concepts.\n\n"
    
    if len(key_terms) > 1:
        summary += f"Q2: What key concepts are covered?\n"
        summary += f"A2: The document covers {', '.join(key_terms[:3])} among other important topics.\n\n"
    
    if len(sentences) > 5:
        summary += f"Q3: What is explained in the document?\n"
        summary += f"A3: {sentences[1] if len(sentences) > 1 else sentences[0]}.\n\n"
    
    summary += f"Q4: How much content is in this document?\n"
    summary += f"A4: The document contains approximately {len(sentences)} sentences covering various aspects of the topic.\n\n"
    
    if len(key_terms) > 2:
        summary += f"Q5: What makes this document valuable?\n"
        summary += f"A5: It provides comprehensive information about {key_terms[0]} and explores related concepts like {key_terms[1]} and {key_terms[2]}.\n"
    
    return summary if summary else "Document uploaded successfully. Content extracted."
