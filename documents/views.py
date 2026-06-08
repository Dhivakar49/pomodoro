from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Document
from ai_engine.text_extractor import extract_text
from ai_engine.summarizer import summarize
from ai_engine.summarizer_hf import summarize_with_hf
from ai_engine.quiz_generator import generate_quiz
import os

@api_view(['GET'])
def list_documents(request):
    """List all uploaded documents"""
    documents = Document.objects.all().order_by('-uploaded_at')
    docs_data = [{
        'id': doc.id,
        'title': doc.title,
        'file_name': doc.file.name if doc.file else '',
        'uploaded_at': doc.uploaded_at
    } for doc in documents]
    return Response(docs_data)

@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_document(request):
    try:
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=400)

        file = request.FILES['file']
        
        # Create document first
        doc = Document.objects.create(
            file=file,
            title=file.name,
            extracted_text=""
        )
        
        # Extract text from the uploaded file
        try:
            text = extract_text(file)
            
            # Choose AI provider based on environment variable
            ai_provider = os.getenv("AI_PROVIDER", "huggingface").lower()
            
            if ai_provider == "openai" and os.getenv("OPENAI_API_KEY"):
                summary = summarize(text)
                quiz = generate_quiz(text)
            elif ai_provider == "huggingface" or os.getenv("HF_API_KEY"):
                summary = summarize_with_hf(text)
                quiz = generate_quiz(text)
            else:
                summary = summarize(text)  # Falls back to mock
                quiz = generate_quiz(text)
                
        except Exception as e:
            text = ""
            summary = f"Error processing file: {str(e)}"
            quiz = "Could not generate quiz questions."

        return Response({
            "message": "File uploaded successfully",
            "file_id": doc.id,
            "file_name": doc.file.name,
            "summary": summary,
            "quiz": quiz,
            "extracted_text_length": len(text),
            "ai_provider": os.getenv("AI_PROVIDER", "huggingface")
        })
    except Exception as e:
        return Response({"error": f"Upload error: {str(e)}"}, status=500)
@csrf_exempt
@api_view(['DELETE'])
def delete_document(request, doc_id):
    try:
        document = Document.objects.get(id=doc_id)
        if document.file:
            document.file.delete()
        document.delete()
        return Response({"message": "Document deleted successfully"}, status=200)
    except Document.DoesNotExist:
        return Response({"error": "Document not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
