from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Exam, Question


class StudentRegistrationForm(UserCreationForm):
    full_name = forms.CharField(required=True, label="Full Name", help_text="You can use your real name here.")
    email = forms.EmailField(required=True, label="Email Address")
    profile_pic = forms.ImageField(required=True, label="Profile Picture")

    class Meta:
        model = User
        fields = ("email", "full_name")
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["full_name"]
        if commit:
            user.save()
        return user

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'description', 'duration_minutes', 'pass_marks']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'option1', 'option2', 'option3', 'option4', 'correct_answer', 'marks']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2}),
        }

class QuestionUploadForm(forms.Form):
    exam = forms.ModelChoiceField(queryset=None, label="Select Exam")
    file = forms.FileField(label="Excel/CSV File")

    def __init__(self, *args, **kwargs):
        from .models import Exam
        super().__init__(*args, **kwargs)
        self.fields['exam'].queryset = Exam.objects.all()

