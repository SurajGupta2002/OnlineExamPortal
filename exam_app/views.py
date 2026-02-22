import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils import timezone
from .models import Exam, Question, Attempt, StudentProfile
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
import pandas as pd
from django.db.models import Avg, Count
from .forms import StudentRegistrationForm, QuestionUploadForm, ExamForm, QuestionForm
from django.contrib.auth.models import User

def landing(request):
    return render(request, 'landing.html')

from django.db import transaction

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    profile_pic = form.cleaned_data.get('profile_pic')
                    StudentProfile.objects.create(user=user, profile_pic=profile_pic)
                messages.success(request, "Registration successful! Please login to continue.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"An error occurred during registration: {str(e)}")
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def home(request):
    exams = Exam.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'exams': exams})

@login_required
def exam_instructions(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    return render(request, 'exam_instructions.html', {'exam': exam})

@login_required
def start_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Check if user has an active attempt or create a new one
    attempt = Attempt.objects.create(user=request.user, exam=exam)
    
    # Randomize questions for this attempt
    questions = list(exam.questions.all())
    random.shuffle(questions)
    
    context = {
        'exam': exam,
        'questions': questions,
        'attempt': attempt,
        'time_remaining': exam.duration_minutes * 60
    }
    return render(request, 'start_exam.html', context)

@login_required
def submit_exam(request, attempt_id):
    if request.method != 'POST':
        return redirect('home')
        
    attempt = get_object_or_404(Attempt, id=attempt_id, user=request.user)
    
    if attempt.is_submitted:
        messages.warning(request, "This attempt has already been submitted.")
        return redirect('results')
        
    # Server-side time validation
    elapsed_time = (timezone.now() - attempt.started_at).total_seconds()
    if elapsed_time > (attempt.exam.duration_minutes * 60) + 10: # 10s grace period
        messages.error(request, "Time limit exceeded. Submission late.")
    
    score = 0
    correct_count = 0
    total_marks = 0
    questions = attempt.exam.questions.all()
    total_questions = questions.count()
    
    for question in questions:
        total_marks += question.marks
        answer_key = f'question_{question.id}'
        selected_option = request.POST.get(answer_key)
        
        if selected_option and int(selected_option) == question.correct_answer:
            score += question.marks
            correct_count += 1
            
    attempt.score = score
    attempt.completed_at = timezone.now()
    attempt.is_submitted = True
    attempt.save()
    
    percentage = (score / total_marks * 100) if total_marks > 0 else 0
    
    context = {
        'attempt': attempt,
        'score': score,
        'total_marks': total_marks,
        'correct_count': correct_count,
        'total_questions': total_questions,
        'percentage': percentage,
    }
    return render(request, 'result_detail.html', context)

@login_required
def results(request):
    attempts = Attempt.objects.filter(user=request.user, is_submitted=True).order_by('-completed_at')
    return render(request, 'results.html', {'attempts': attempts})


@staff_member_required
def admin_dashboard(request):
    total_exams = Exam.objects.count()
    total_students = User.objects.filter(is_staff=False).count()
    total_attempts = Attempt.objects.count()
    total_questions = Question.objects.count()
    
    recent_attempts = Attempt.objects.filter(is_submitted=True).order_by('-completed_at')[:5]
    
    context = {
        'total_exams': total_exams,
        'total_students': total_students,
        'total_attempts': total_attempts,
        'total_questions': total_questions,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'admin_dashboard.html', context)

@staff_member_required
def admin_exams(request):
    exams = Exam.objects.annotate(q_count=Count('questions'))
    return render(request, 'admin_exams.html', {'exams': exams})

@staff_member_required
def admin_exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam created successfully!")
            return redirect('admin_exams')
    else:
        form = ExamForm()
    return render(request, 'admin_exam_form.html', {'form': form, 'title': 'Create Exam'})

@staff_member_required
def admin_exam_edit(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam updated successfully!")
            return redirect('admin_exams')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'admin_exam_form.html', {'form': form, 'title': 'Edit Exam', 'exam': exam})

@staff_member_required
def admin_exam_questions(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            messages.success(request, "Question added successfully!")
            return redirect('admin_exam_questions', exam_id=exam.id)
    else:
        form = QuestionForm()
        
    return render(request, 'admin_questions.html', {
        'exam': exam,
        'questions': questions,
        'form': form
    })

@staff_member_required
def admin_exam_delete(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    exam.delete()
    messages.success(request, "Exam deleted successfully!")
    return redirect('admin_exams')

@staff_member_required
def admin_question_delete(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    exam_id = question.exam.id
    question.delete()
    messages.success(request, "Question deleted successfully!")
    return redirect('admin_exam_questions', exam_id=exam_id)

@staff_member_required
def admin_students(request):

    students = User.objects.filter(is_staff=False).annotate(
        attempt_count=Count('attempt'),
        avg_score=Avg('attempt__score')
    )
    return render(request, 'admin_students.html', {'students': students})

@staff_member_required
def admin_results(request):
    attempts = Attempt.objects.filter(is_submitted=True).order_by('-completed_at')
    return render(request, 'admin_results.html', {'attempts': attempts})

@staff_member_required
def upload_questions(request):
    if request.method == 'POST':
        form = QuestionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            exam = form.cleaned_data['exam']
            file = request.FILES['file']
            
            try:
                # Support CSV and Excel
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                
                # Expected columns: text, option1, option2, option3, option4, correct_answer, marks
                created_count = 0
                for _, row in df.iterrows():
                    Question.objects.create(
                        exam=exam,
                        text=row['text'],
                        option1=row['option1'],
                        option2=row['option2'],
                        option3=row['option3'],
                        option4=row['option4'],
                        correct_answer=int(row['correct_answer']),
                        marks=int(row.get('marks', 1))
                    )
                    created_count += 1
                
                messages.success(request, f"Successfully uploaded {created_count} questions!")
                return redirect('admin_dashboard') # Redirect to admin dashboard
            except Exception as e:
                messages.error(request, f"Error processing file: {str(e)}")
    else:
        form = QuestionUploadForm()
    
    return render(request, 'upload_questions.html', {'form': form})

