from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('exam/<int:exam_id>/instructions/', views.exam_instructions, name='exam_instructions'),
    path('exam/<int:exam_id>/start/', views.start_exam, name='start_exam'),
    path('attempt/<int:attempt_id>/submit/', views.submit_exam, name='submit_exam'),
    path('results/', views.results, name='results'),
    
    # Custom Admin Dashboard URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/exams/', views.admin_exams, name='admin_exams'),
    path('admin/exams/create/', views.admin_exam_create, name='admin_exam_create'),
    path('admin/exams/<int:exam_id>/edit/', views.admin_exam_edit, name='admin_exam_edit'),
    path('admin/exams/<int:exam_id>/delete/', views.admin_exam_delete, name='admin_exam_delete'),
    path('admin/exams/<int:exam_id>/questions/', views.admin_exam_questions, name='admin_exam_questions'),
    path('admin/questions/<int:question_id>/delete/', views.admin_question_delete, name='admin_question_delete'),
    path('admin/students/', views.admin_students, name='admin_students'),

    path('admin/results/', views.admin_results, name='admin_results'),
    path('admin/upload/', views.upload_questions, name='upload_questions'), # Reusing existing
]

