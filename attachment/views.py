from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from .forms import *

# Create your views here.
def register(request):
    
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form  = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    
    return render(request, 'attachment/register.html',context)
    
def login_view(request):
    user = authenticate(request, email="test@gmail.com", password="password@123")
    if user is not None:
            login(request, user)
    
    return render(request, 'attachment/login.html')
    

def update_logbook(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        description = request.POST.get('description')
        LogBook.objects.create(
            date = date,
            description = description,
            student =  request.user.student
        )
    return render(request, 'attachment/update_logbook.html')

def weekly_summary(request):
    pass