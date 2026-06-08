from django.db import models
from tasks.models import Subject

class PomodoroSession(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    duration = models.IntegerField(default=25)  # 25 minute pomodoro
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.duration} min"
