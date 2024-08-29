from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.

def sign_up(request):
    if request.method == 'GET':
        return render(request, 'sign_up.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return redirect('inventory')
                # return HttpResponse('User created successfully')
            except:
                return render(request, 'sign_up.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        return render(request, 'sign_up.html', {
                    'form': UserCreationForm,
                    'error': 'Passwords do not match'
                })
def template_access(request):
    return render(request, 'template.html')
            
        
        
    

