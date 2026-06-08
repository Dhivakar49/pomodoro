from django.urls import path
from .views import upload_document, list_documents, delete_document

urlpatterns = [
    path('upload/', upload_document),
    path('', list_documents),  # GET /api/documents/
    path('<int:doc_id>/', delete_document),  # DELETE /api/documents/<id>/
]
