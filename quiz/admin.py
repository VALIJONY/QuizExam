# quiz/admin.py
from django.contrib import admin
from .models import Subject, Question, ExamResult

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'subject', 'correct_answer')
    list_filter = ('subject',) # Fanga qarab filtrlash imkoniyati
    search_fields = ('text',)

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('get_student_name', 'subject', 'score', 'date_taken')
    list_filter = ('subject', 'date_taken') # Fan va sana bo'yicha filtrlash
    search_fields = ('student__username',)

    def get_student_name(self, obj):
        return obj.student.username
    get_student_name.short_description = "O'quvchi"