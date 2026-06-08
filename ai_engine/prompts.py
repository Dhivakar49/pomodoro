SUMMARY_PROMPT = """
Create a comprehensive study summary for a student audience.

Requirements:
1. Main Summary (200-300 words):
   - Use clear, simple language
   - Cover all key concepts and important facts
   - Explain complex terms in simple ways
   - Use bullet points for clarity

2. Important Questions & Answers (5-7 Q&A pairs):
   - Extract the most critical information as Q&A
   - Questions should be clear and specific
   - Answers should be concise but complete
   - Format as:
     Q1: [Question]
     A1: [Answer]

Format your response with the summary first, followed by the Q&A pairs. Do not use markdown headers (###) or asterisks for formatting. Keep it simple and clean.

Content:
"""


QUIZ_PROMPT = """
Generate 5 MCQs from this content:
"""
