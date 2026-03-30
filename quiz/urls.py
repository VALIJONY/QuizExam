# quiz/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Avtorizatsiya URL'lari
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Asosiy platforma URL'lari
    path('', views.HomeView.as_view(), name='home'),
    path('learn/<int:subject_id>/', views.LearnModeView.as_view(), name='learn_mode'),
    path('exam/<int:subject_id>/', views.ExamModeView.as_view(), name='exam_mode'),
    
    path('api/check-answer/<int:question_id>/', views.CheckAnswerView.as_view(), name='check_answer'),
    path('result/', views.ExamResultView.as_view(), name='exam_result'),
    
    # Admin Dashboard URL'lari
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Questions CRUD
    path('dashboard/questions/', views.QuestionListView.as_view(), name='question_list'),
    path('dashboard/questions/add/', views.QuestionCreateView.as_view(), name='question_add'),
    path('dashboard/questions/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='question_edit'),
    path('dashboard/questions/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    
    # Subjects CRUD
    path('dashboard/subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('dashboard/subjects/add/', views.SubjectCreateView.as_view(), name='subject_add'),
    path('dashboard/subjects/<int:pk>/edit/', views.SubjectUpdateView.as_view(), name='subject_edit'),
    path('dashboard/subjects/<int:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),
]