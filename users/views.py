from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# from .forms import CustomUserCreationForm, CustomAuthenticationForm
from courses.models import Course, Enrollment
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'users/register.html')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'users/register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'users/register.html')

        # Create new user
        user = User.objects.create_user(
            username=username,
            first_name=fname,
            last_name=lname,
            email=email,
            password=password1
        )
        user.save()

        # Log the user in
        login(request, user)
        messages.success(request, 'Registration successful. You are now logged in.')
        return redirect('users:dashboard')

    return render(request, 'users/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        my_user = authenticate(username=username, password=password)

        if my_user is not None:
            login(request, my_user)
            messages.success(request, 'Login successful.')
            # Redirect to dashboard or courses list
            return redirect('users:dashboard')  # Change to 'dashboard' or 'courses_list' as needed
            
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'users/login.html')

    return render(request, 'users/login.html')
    
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('users:login') # Redirect to login page after logout



@login_required
def dashboard(request):
    enrolled_courses = Enrollment.objects.filter(user=request.user)
    context = {
        'enrolled_courses': enrolled_courses,
    }
    return render(request, 'users/dashboard.html', context)