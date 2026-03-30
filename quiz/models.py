# quiz/models.py
from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Fan nomi")
    description = models.TextField(verbose_name="Fan tavsifi", blank=True)
    
    def __str__(self):
        return self.name

class Question(models.Model):
    ANSWER_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Fan")
    text = models.TextField(verbose_name="Savol matni")
    option_a = models.CharField(max_length=255, verbose_name="A varianti")
    option_b = models.CharField(max_length=255, verbose_name="B varianti")
    option_c = models.CharField(max_length=255, verbose_name="C varianti")
    option_d = models.CharField(max_length=255, verbose_name="D varianti")
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES, verbose_name="To'g'ri javob")

    def __str__(self):
        return f"{self.subject.name} - {self.text[:50]}..."

class ExamResult(models.Model):
    # student_name o'rniga haqiqiy User modelini bog'ladik
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="O'quvchi")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Fan")
    score = models.IntegerField(verbose_name="To'g'ri javoblar soni")
    total_questions = models.IntegerField(default=30, verbose_name="Umumiy savollar")
    date_taken = models.DateTimeField(auto_now_add=True, verbose_name="Topshirilgan vaqt")

    def __str__(self):
        return f"{self.student.username} - {self.subject.name} - {self.score}/{self.total_questions}"