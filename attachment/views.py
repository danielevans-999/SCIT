from django.shortcuts import render
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
    pass