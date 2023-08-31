from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import timedelta
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

@login_required
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

@login_required
def weekly_summary(request):
    if not request.user.updated_profile:
        return redirect('student_registration')
    
    current_user = request.user
    default_week = "week 1"
    logbooks = None
    student = Student.objects.get(user = current_user)
    start = student.start_date
   
     
    week = request.GET.get('week')
    if week == 'week 1':
        logbooks = LogBook.objects.filter(date__range=(start, start + timedelta(days = 8)), student = student).order_by('date')
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 2':
        logbooks =  LogBook.objects.filter(date__range=(start + timedelta(days = 8), start + timedelta(days = 15)), student = student).order_by('date')
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 3':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 15), start + timedelta(days = 22)), student = student).order_by('date')
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 4':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 22), start + timedelta(days = 29)), student = student).order_by('date')
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 5':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 29), start + timedelta(days = 36)), student = student).order_by('date')
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 6':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 36), start + timedelta(days = 43)), student = student).order_by('date')
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 7':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 43), start + timedelta(days = 50)), student = student).order_by('date')
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 8':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 50), start + timedelta(days = 57)), student = student).order_by('date')
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 9':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 57), start + timedelta(days = 64)), student = student).order_by('date')
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 10':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 64), start + timedelta(days = 71)), student = student).order_by('date')
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 11':
        logbooks =LogBook.objects.filter(date__range=(start + timedelta(days = 71), start + timedelta(days = 78)), student = student).order_by('date')
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
    
    elif week == 'week 12':
        logbooks = LogBook.objects.filter(date__range=(start + timedelta(days = 78), start + timedelta(days = 85)), student = student).order_by('date')
        print(logbooks)
        return render(request, 'attachment/summary.html', locals())
   
    logbooks = LogBook.objects.filter(date__range=(start, start + timedelta(days = 8)), student = student).order_by('date')
    return render(request, 'attachment/summary.html', locals())

@login_required
def edit_logbook(request, id):
    logbook = get_object_or_404(LogBook, id = id)
    
    if request.method == 'POST':
        description = request.POST.get('update_desc')
        logbook.description = description
        logbook.save()
        return redirect('summary')
        
@login_required
def student_registration(request):
    current_user = request.user
    status = current_user.updated_profile
    try:
        student = Student.objects.get(user = current_user)
    except Student.DoesNotExist:
        student = None
    print(student)
    if request.method == 'POST':
        name = request.POST.get('name')
        registration_number = request.POST.get('registration_number')
        course = request.POST.get('course')
        year = int(request.POST.get('year'))
        department = request.POST.get('department')
        organisation = request.POST.get('organisation')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        photo_url = request.FILES.get('pic')

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
                user = current_user,
                photo_url = photo_url

            )
            
            profile.user.updated_profile = True
            current_user.save()
            return redirect('summary')

    return render(request, 'attachment/student_registration.html', locals())

@login_required
def uploads(request):
    if not request.user.updated_profile:
        return redirect('student_registration')
    
    student = request.user.student
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        uploaded_pdf = Reports.objects.create(student = student, pdf_file = pdf_file)
        uploaded_pdf.save()
    return render(request, "attachment/uploads.html")

def logout_view(request):
    logout(request)
    return redirect('login')