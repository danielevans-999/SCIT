from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import *

# Create your views here.
def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}

    return render(request, 'attachment/register.html', context)


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'student':
                return redirect('summary')

    return render(request, 'attachment/login.html')


def update_logbook(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        description = request.POST.get('description')
        LogBook.objects.create(
            date=date,
            description=description,
            student=request.user.student
        )
    return render(request, 'attachment/update_logbook.html')


def weekly_summary(request):
    return render(request, 'attachment/summary.html')
