from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from .models import Course, Enrollment, Lesson, Quiz, Question, Choice, UserAnswer, Feedback
from .forms import EnrollmentForm, FeedbackForm, LessonForm, QuizForm, QuestionForm, ChoiceForm
from django.contrib import messages

def course_list(request):
    #check if user is not login
    # courses = Course.objects.all().order_by('title')
    if request.user.is_authenticated:
        # If logged in, run the more complex query to check for enrollment
        courses = Course.objects.annotate(
            is_enrolled=Exists(
                Enrollment.objects.filter(
                    user=request.user, 
                    course=OuterRef('pk')
                )
            )
        )
    else:
        # If not logged in, just use the simple query
        # No enrollment information is needed for an anonymous user
        courses = Course.objects.all().order_by('title')
    context = {'courses': courses}
    return render(request, 'courses/course_list.html', context)

# @login_required
def course_detail(request, course_slug):
    course = get_object_or_404(Course, id=course_slug)
    # is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    course_slug = course.course_slug  # Use the slug field for URL
    lessons = course.lessons.all().order_by('order')
    quizzes = course.quizzes.all()
    feedback_form = FeedbackForm()
    feedbacks = course.feedbacks.all().order_by('-submitted_at')

    context = {
        'course': course,
        'course_slug': course_slug,  # Use the slug field for URL
        # 'is_enrolled': is_enrolled,
        'lessons': lessons,
        'quizzes': quizzes,
        'feedback_form': feedback_form,
        'feedbacks': feedbacks,
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        # You can add a hidden form field or just rely on URL for course_id
        if not Enrollment.objects.filter(user=request.user, course=course).exists():
            Enrollment.objects.create(user=request.user, course=course)
            messages.success(request, f'You have successfully enrolled in {course.title}.')
            return redirect('dashboard') # Or redirect to course_detail
        else:
            # Already enrolled
            messages.info(request, f'You are already enrolled in {course.title}.')
            # Optionally redirect to course detail or dashboard
            return redirect('course_detail', course_id=course.id)
    return redirect('course_detail', course_id=course.id) # If GET request

@login_required
def lesson_detail(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    # Ensure user is enrolled to view lessons
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.error(request, 'You must be enrolled in the course to view lessons.')
        return redirect('course_detail', course_id=course.id) # Or show an error

    context = {
        'course': course,
        'lesson': lesson,
    }
    return render(request, 'courses/lesson_detail.html', context)

@login_required
def quiz_detail(request, course_id, quiz_id):
    course = get_object_or_404(Course, id=course_id)
    quiz = get_object_or_404(Quiz, id=quiz_id, course=course)
    questions = quiz.questions.all()

    if request.method == 'POST':
        # Process quiz submission
        for question in questions:
            if question.question_type == 'MCQ':
                selected_choice_id = request.POST.get(f'question_{question.id}')
                if selected_choice_id:
                    selected_choice = get_object_or_404(Choice, id=selected_choice_id)
                    UserAnswer.objects.update_or_create(
                        user=request.user,
                        question=question,
                        defaults={'selected_choice': selected_choice}
                    )
            elif question.question_type == 'Text':
                text_answer = request.POST.get(f'question_{question.id}_text')
                UserAnswer.objects.update_or_create(
                    user=request.user,
                    question=question,
                    defaults={'text_answer': text_answer}
                )
        messages.success(request, 'Quiz submitted successfully.')
        return redirect('quiz_results', course_id=course.id, quiz_id=quiz.id) # Redirect to results or back to course detail
    
    context = {
        'course': course,
        'quiz': quiz,
        'questions': questions,
    }
    
    return render(request, 'courses/quiz_detail.html', context)

@login_required
def quiz_results(request, course_id, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    user_answers = UserAnswer.objects.filter(user=request.user, question__in=questions)

    score = 0
    total_questions = questions.count()
    results = []

    for question in questions:
        user_answer = user_answers.filter(question=question).first()
        is_correct = False
        correct_answer = None

        if question.question_type == 'MCQ':
            correct_choice = question.choices.filter(is_correct=True).first()
            if user_answer and user_answer.selected_choice == correct_choice:
                is_correct = True
                score += 1
            correct_answer = correct_choice.text if correct_choice else "N/A"
        elif question.question_type == 'Text':
            # For text answers, you might need manual grading or specific logic
            # For simplicity, we'll just show the user's answer
            correct_answer = "Evaluated manually" # Or define a correct answer in model
            if user_answer and user_answer.text_answer:
                pass # Logic to check correctness if auto-gradable
            is_correct = None # Cannot auto-grade here
        
        results.append({
            'question': question,
            'user_answer': user_answer,
            'is_correct': is_correct,
            'correct_answer': correct_answer,
        })
    
    context = {
        'quiz': quiz,
        'results': results,
        'score': score,
        'total_questions': total_questions,
    }
    return render(request, 'courses/quiz_results.html', context)

@login_required
def submit_feedback(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.course = course
            feedback.save()
            return redirect('course_detail', course_id=course.id)
    return redirect('course_detail', course_id=course.id)