# urls.py (at project level)
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, 'error_pages/404.html', status=404)

def custom_500(request):
    return render(request, 'error_pages/500.html', status=500)

def custom_403(request, exception):
    return render(request, 'error_pages/403.html', status=403)

def custom_400(request, exception):
    return render(request, 'error_pages/400.html', status=400)

handler404 = 'StudyBuddy.urls.custom_404'
handler500 = 'StudyBuddy.urls.custom_500'
handler403 = 'StudyBuddy.urls.custom_403'
handler400 = 'StudyBuddy.urls.custom_400'
