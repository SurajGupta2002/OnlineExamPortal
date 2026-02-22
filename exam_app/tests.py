from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Exam, Question, Attempt

class ScoringTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='password123')
        self.exam = Exam.objects.create(title='Logic Test', duration_minutes=10)
        self.q1 = Question.objects.create(
            exam=self.exam, text='1 + 1?', 
            option1='1', option2='2', option3='3', option4='4', 
            correct_answer=2, marks=1
        )
        self.q2 = Question.objects.create(
            exam=self.exam, text='2 + 2?', 
            option1='2', option2='3', option3='4', option4='5', 
            correct_answer=3, marks=1
        )
        self.client = Client()
        self.client.login(username='teststudent', password='password123')

    def test_scoring_logic(self):
        attempt = Attempt.objects.create(user=self.user, exam=self.exam)
        url = reverse('submit_exam', args=[attempt.id])
        
        # Post answers: Q1 correct, Q2 wrong
        response = self.client.post(url, {
            f'question_{self.q1.id}': '2',
            f'question_{self.q2.id}': '1'
        })
        
        attempt.refresh_from_db()
        self.assertEqual(attempt.score, 1)
        self.assertTrue(attempt.is_submitted)
        self.assertRedirects(response, reverse('results'))

    def test_all_correct(self):
        attempt = Attempt.objects.create(user=self.user, exam=self.exam)
        url = reverse('submit_exam', args=[attempt.id])
        
        response = self.client.post(url, {
            f'question_{self.q1.id}': '2',
            f'question_{self.q2.id}': '3'
        })
        
        attempt.refresh_from_db()
        self.assertEqual(attempt.score, 2)
