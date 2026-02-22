from django.contrib import admin, messages
from .models import Exam, Question, Attempt, StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
from django import forms
import pandas as pd
import io

class ExamAdminForm(forms.ModelForm):
    question_file = forms.FileField(
        required=False, 
        label="Bulk Upload Questions (Excel/CSV)",
        help_text="Upload an Excel or CSV file to automatically add questions to this exam."
    )

    class Meta:
        model = Exam
        fields = '__all__'

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    form = ExamAdminForm
    list_display = ('title', 'duration_minutes', 'created_at')
    inlines = [QuestionInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Handle bulk upload if a file was provided
        file = request.FILES.get('question_file')
        if file:
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                
                # Required columns match the previous logic
                created_count = 0
                for _, row in df.iterrows():
                    Question.objects.create(
                        exam=obj,
                        text=row['text'],
                        option1=row['option1'],
                        option2=row['option2'],
                        option3=row['option3'],
                        option4=row['option4'],
                        correct_answer=int(row['correct_answer']),
                        marks=int(row.get('marks', 1))
                    )
                    created_count += 1
                
                self.message_user(request, f"Successfully imported {created_count} questions from the file.", messages.SUCCESS)
            except Exception as e:
                self.message_user(request, f"Error importing questions: {str(e)}", messages.ERROR)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'exam', 'correct_answer', 'marks')
    list_filter = ('exam',)

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'score', 'started_at', 'is_submitted')
    list_filter = ('exam', 'user', 'is_submitted')
