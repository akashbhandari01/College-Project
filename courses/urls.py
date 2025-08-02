from django.urls import path
from .import views

urlpatterns = [
    path('', views.course_list, name='courses_list'),
    # path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('<int:course_id>/quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('<int:course_id>/quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
    path('<int:course_id>/feedback/submit/', views.submit_feedback, name='submit_feedback'),
]

app_name = 'courses'