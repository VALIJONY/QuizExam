from django.shortcuts import render

# Create your views here.
# quiz/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, View, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
import json
from .models import Question, ExamResult, Subject

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('home') 

class HomeView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'home.html'
    context_object_name = 'subjects'


class LearnModeView(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'quiz/learn.html'
    context_object_name = 'questions'
    
    def get_queryset(self):
        subject_id = self.kwargs['subject_id']
        return Question.objects.filter(subject_id=subject_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, id=self.kwargs['subject_id'])
        return context

class CheckAnswerView(LoginRequiredMixin, View):
    def post(self, request, question_id):
        try:
            data = json.loads(request.body)
            selected_option = data.get('option')
            question = get_object_or_404(Question, id=question_id)
            
            is_correct = (selected_option == question.correct_answer)
            return JsonResponse({
                'is_correct': is_correct,
                'correct_answer': question.correct_answer
            })
        except Exception:
            return JsonResponse({'error': 'Xatolik yuz berdi'}, status=400)

class ExamModeView(LoginRequiredMixin, View):
    def get(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)
        # Har doim 30 ta tasodifiy savol beramiz
        questions = Question.objects.filter(subject=subject).order_by('?')[:30]
        return render(request, 'quiz/exam.html', {'questions': questions, 'subject': subject})

    def post(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)
        score = 0
        for key, value in request.POST.items():
            if key.startswith('question_'):
                q_id = int(key.split('_')[1])
                question = Question.objects.get(id=q_id)
                if value == question.correct_answer:
                    score += 1
        
        ExamResult.objects.create(
            student=request.user,
            subject=subject,
            score=score,
            total_questions=30
        )
        return redirect('exam_result')

class ExamResultView(LoginRequiredMixin, TemplateView):
    template_name = 'quiz/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # O'quvchining so'nggi natijasini olib beramiz
        context['result'] = ExamResult.objects.filter(student=self.request.user).latest('date_taken')
        return context





class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

# --- ADMIN CRUD KLASSLARI ---
class DashboardView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Barcha statik ma'lumotlarni Dashboard uchun yig'amiz
        context['subjects_count'] = Subject.objects.count()
        context['questions_count'] = Question.objects.count()
        context['students_count'] = User.objects.filter(is_superuser=False).count()
        # Oxirgi qo'shilgan savollarni ro'yxatda ko'rsatish uchun
        context['questions'] = Question.objects.select_related('subject').order_by('-id')[:50]
        return context

class QuestionCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Question
    template_name = 'question_form.html'
    fields = ['subject', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
    success_url = reverse_lazy('dashboard')

class QuestionListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Question
    template_name = 'question_list.html'
    context_object_name = 'questions'
    paginate_by = 20

    def get_queryset(self):
        return Question.objects.select_related('subject').order_by('-id')

class QuestionUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Question
    template_name = 'question_form.html'
    fields = ['subject', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
    success_url = reverse_lazy('question_list')

class QuestionDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Question
    template_name = 'question_confirm_delete.html'
    success_url = reverse_lazy('question_list')

class SubjectCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Subject
    template_name = 'subject_form.html'
    fields = ['name']
    success_url = reverse_lazy('dashboard')

class SubjectListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Subject
    template_name = 'subject_list.html'
    context_object_name = 'subjects'
    paginate_by = 20

    def get_queryset(self):
        return Subject.objects.order_by('-id')

class SubjectUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Subject
    template_name = 'subject_form.html'
    fields = ['name']
    success_url = reverse_lazy('subject_list')

class SubjectDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Subject
    template_name = 'subject_confirm_delete.html'
    success_url = reverse_lazy('subject_list')

