from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    total_questions = models.PositiveIntegerField(default=0)
    pass_marks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    
    CHOICES = (
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
        (4, 'Option 4'),
    )
    correct_answer = models.PositiveIntegerField(choices=CHOICES)
    marks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.text[:50]

class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(default=0)
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.exam.title}"

    @property
    def time_remaining(self):
        if self.is_submitted:
            return 0
        elapsed_time = (timezone.now() - self.started_at).total_seconds()
        remaining = (self.exam.duration_minutes * 60) - elapsed_time
        return max(0, int(remaining))
