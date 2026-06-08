from django.urls import path
from .views import start_session, complete_session, list_subjects,save_pomodoro,get_stats

urlpatterns = [
    path('start/', start_session),
    path('complete/', complete_session),
    path('subjects/', list_subjects),
    path('save/', save_pomodoro),
    path('stats/', get_stats),
]
