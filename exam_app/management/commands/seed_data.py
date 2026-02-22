from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from exam_app.models import Exam, Question

class Command(BaseCommand):
    help = 'Seeds initial data for the Online Exam System'

    def handle(self, *args, **kwargs):
        # Create Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
            self.stdout.write(self.style.SUCCESS('Successfully created superuser: admin/adminpass'))

        # Create Sample Exam 1
        exam1, created = Exam.objects.get_or_create(
            title='General Knowledge Quiz',
            description='A basic quiz covering various general knowledge topics.',
            duration_minutes=5,
            pass_marks=3
        )
        if created:
            Question.objects.create(exam=exam1, text='What is the capital of France?', option1='London', option2='Berlin', option3='Paris', option4='Madrid', correct_answer=3)
            Question.objects.create(exam=exam1, text='Which planet is known as the Red Planet?', option1='Venus', option2='Mars', option3='Jupiter', option4='Saturn', correct_answer=2)
            Question.objects.create(exam=exam1, text='What is the largest ocean on Earth?', option1='Atlantic', option2='Indian', option3='Pacific', option4='Arctic', correct_answer=3)
            Question.objects.create(exam=exam1, text='Who wrote "Romeo and Juliet"?', option1='Dickens', option2='Shakespeare', option3='Hemingway', option4='Austen', correct_answer=2)
            Question.objects.create(exam=exam1, text='What is the boiling point of water?', option1='90C', option2='100C', option3='110C', option4='120C', correct_answer=2)
            self.stdout.write(self.style.SUCCESS('Created Exam 1: General Knowledge Quiz'))

        # Create Sample Exam 2
        exam2, created = Exam.objects.get_or_create(
            title='Python Programming Basics',
            description='Test your fundamental Python knowledge.',
            duration_minutes=10,
            pass_marks=2
        )
        if created:
            Question.objects.create(exam=exam2, text='Which of these is NOT a Python data type?', option1='int', option2='string', option3='boolean', option4='double', correct_answer=4)
            Question.objects.create(exam=exam2, text='How do you start a comment in Python?', option1='//', option2='/*', option3='#', option4='--', correct_answer=3)
            Question.objects.create(exam=exam2, text='Which function is used to get the length of a list?', option1='len()', option2='length()', option3='size()', option4='count()', correct_answer=1)
            Question.objects.create(exam=exam2, text='What is the result of 3 ** 2?', option1='6', option2='9', option3='27', option4='12', correct_answer=2)
            Question.objects.create(exam=exam2, text='Which keyword is used to define a function?', option1='func', option2='define', option3='def', option4='function', correct_answer=3)
            self.stdout.write(self.style.SUCCESS('Created Exam 2: Python Programming Basics'))
