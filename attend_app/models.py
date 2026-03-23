import datetime

from django.db import models
from django.utils import timezone

class Worker(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True, blank=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in_time = models.TimeField(default=timezone.now)
    signature = models.CharField(max_length=255, blank=True, help_text="Worker's signature or confirmation")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['worker', 'date']  # one attendance per worker per day

    def __str__(self):
        return f"{self.worker.name} - {self.date} - {self.check_in_time}"

    def is_late(self):
        # Consider 9:00 AM as the cutoff
        cutoff = datetime.time(9, 0, 0)
        return self.check_in_time > cutoff
