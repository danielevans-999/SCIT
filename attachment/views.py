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
    if not request.user.updated_profile:
        return redirect('student_registration')
    
    return render(request, 'attachment/summary.html')


def student_registration(request):
    current_user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        registration_number = request.POST.get('registration_number')
        course = request.POST.get('course')
        year = int(request.POST.get('year'))
        department = request.POST.get('department')
        organisation = request.POST.get('organisation')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if not current_user.updated_profile:

            profile = Student.objects.create(

                name=name,
                registration_number=registration_number,
                course=course,
                year=year,
                department=department,
                organisation=organisation,
                start_date=start_date,
                end_date=end_date,
                user = current_user

            )
            
            profile.user.updated_profile = True
            current_user.save()
            return redirect('summary')

    return render(request, 'attachment/student_registration.html', locals())
