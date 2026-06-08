from django.db import models

class StudyStat(models.Model):
    date = models.DateField()
    pomodoros = models.IntegerField(default=0)
    focus_score = models.FloatField(default=0)

    def __str__(self):
        return f"{self.date} - {self.pomodoros} pomodoros"
