import os
from openai import OpenAI
from .prompts import SUMMARY_PROMPT

def summarize(text):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return "Mock Summary: AI key not configured."

    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": SUMMARY_PROMPT + text[:5000]}
            ]
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"
