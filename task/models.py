from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    task_name = models.CharField(max_length=150)
    created_date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False, null=True)
    user  = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name

