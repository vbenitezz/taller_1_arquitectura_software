from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from .forms import Custom_User_Creation_Form,Custom_Login_Form
from django.contrib import messages
from .models import Restaurant_Chain, Foundation
from django.shortcuts import get_object_or_404
from .models import Restaurant_Chain_Branch

def sign_up(request):
    user_type = request.GET.get('user_type') if request.method == 'GET' else request.POST.get('user_type')

    if request.method == 'POST':
        signup_form = Custom_User_Creation_Form(request.POST)
        if signup_form.is_valid():
            print(signup_form.cleaned_data)
            cleaned_data = signup_form.cleaned_data
            user = signup_form.save(commit=False)
            if user_type == 'restaurant chain':
                user = Restaurant_Chain.objects.create(
                    nit=cleaned_data['nit'],
                    name=cleaned_data['name'],
                    email=cleaned_data['email']
                )
                user.set_password(cleaned_data['password1'])
                user.save()
            elif user_type == 'foundation':
                user = Foundation.objects.create(
                    nit=cleaned_data['nit'],
                    name=cleaned_data['name'],
                    email=cleaned_data['email']
                )
                user.set_password(cleaned_data['password1'])
                user.save()

            user = authenticate(username=cleaned_data['email'], password=cleaned_data['password1'])
            if user is not None:
                login(request,user)
                return redirect('select_branch' if user_type == 'restaurant chain' else 'view_products_for_donate')
            else:
                messages.error(request, 'Authentication failed. Please check your credentials.')
        else:
            print(signup_form.errors)
            messages.error(request, "Invalid form. Please check the errors below")
            for field, errors in signup_form.errors.items():
                for error in errors:
                    messages.error(request, f"Error: {error}")
    else:
        signup_form = Custom_User_Creation_Form()

    return render(request, 'sign_up.html', {'signup_form': signup_form, 'user_type': user_type})


def login_view(request):
    if request.method == 'POST':
        login_form = Custom_Login_Form(request, data=request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {user.name}!')
                return redirect('select_branch' if hasattr(user, 'restaurant_chain') else 'view_products_for_donate')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
            for field, errors in login_form.errors.items():
                for error in errors:
                    messages.error(request, f"Error: {error}")
    else:
        login_form = Custom_Login_Form()

    return render(request, 'login.html', {'login_form': login_form})

def select_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Asegura que el usuario esté autenticado

    branches = Restaurant_Chain_Branch.objects.filter(id_restaurant_chain=request.user)
    if request.method == 'POST':
        branch_id = request.POST.get('branch_id')
        branch = get_object_or_404(Restaurant_Chain_Branch, id=branch_id, id_restaurant_chain=request.user)
        request.user.selected_branch = branch
        request.user.save()
        return redirect('inventory')

    return render(request, 'select_branch.html', {'branches': branches})

def create_branch(request):
    if request.method=="POST":
        user = request.user
        branches = Restaurant_Chain_Branch.objects.filter(id_restaurant_chain=request.user)
        restaurant_chain = get_object_or_404(Restaurant_Chain, email=user.email)
        image = request.FILES['branch_image']
        branch = request.POST['branch_name']
        address = request.POST['branch_address']
        if restaurant_chain.branches.filter(address=address):
            messages.error(request, 'Branch with same address already exists')
            return render(request,'select_branch.html', {'branches': branches})
        
        Restaurant_Chain_Branch.objects.create(
            id_restaurant_chain = restaurant_chain,
            image = image,
            branch = branch,
            address = address
        )

        messages.success(request, 'Branch created sucessfully')
        return redirect('select_branch') 
    else:
        return redirect('select_branch')





