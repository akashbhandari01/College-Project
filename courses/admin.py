from django.contrib import admin
from .models import Course, Enrollment, Lesson, Quiz, Question, Choice, UserAnswer, Feedback

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class QuizInline(admin.TabularInline):
    model = Quiz
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4 # For 4 choices per question

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'created_at')
    search_fields = ('title', 'instructor__username')
    inlines = [LessonInline, QuizInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')
    list_filter = ('course', 'user')
    search_fields = ('user__username', 'course__title')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'lesson')
    list_filter = ('course',)
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'question_type')
    list_filter = ('quiz', 'question_type')
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('question__quiz',)

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selected_choice', 'text_answer', 'submitted_at')
    list_filter = ('user', 'question__quiz')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'submitted_at')
    list_filter = ('course', 'user', 'rating')