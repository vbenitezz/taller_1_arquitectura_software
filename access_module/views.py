from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login

from .forms import Custom_User_Creation_Form, Custom_Login_Form
from .models import Restaurant_Chain, Foundation, Restaurant_Chain_Branch
from .services.implementations import DjangoUserRegistrationService

# -------------------------------------------------------------------
# Inversión de Dependencias
# -------------------------------------------------------------------
class SignUpView(View):
    def __init__(self, registration_service=None):
        # Inyección de dependencia
        self.registration_service = registration_service or DjangoUserRegistrationService()

    def get(self, request):
        user_type = request.GET.get('user_type')
        signup_form = Custom_User_Creation_Form()
        return render(request, 'sign_up.html', {'signup_form': signup_form, 'user_type': user_type})

    def post(self, request):
        user_type = request.POST.get('user_type')
        signup_form = Custom_User_Creation_Form(request.POST)

        if signup_form.is_valid():
            cleaned_data = signup_form.cleaned_data
            user = self.registration_service.register_user(cleaned_data, user_type)
            if not user:
                messages.error(request, "Invalid user type.")
                return render(request, 'sign_up.html', {'signup_form': signup_form, 'user_type': user_type})

            user = authenticate(username=cleaned_data['email'], password=cleaned_data['password1'])
            if user is not None:
                login(request, user)
                redirect_page = 'select_branch' if user_type == 'restaurant chain' else 'view_products_for_donate'
                return redirect(redirect_page)
            else:
                messages.error(request, 'Authentication failed. Please check your credentials.')
        else:
            messages.error(request, "Invalid form. Please check the errors below")
            for field, errors in signup_form.errors.items():
                for error in errors:
                    messages.error(request, f"Error: {error}")

        return render(request, 'sign_up.html', {'signup_form': signup_form, 'user_type': user_type})

class LoginView(View):
    def get(self, request):
        login_form = Custom_Login_Form()
        return render(request, 'login.html', {'login_form': login_form})

    def post(self, request):
        login_form = Custom_Login_Form(request, data=request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {user.name}!')
                return redirect('select_branch' if hasattr(user, 'restaurant_chain') else 'view_products_for_donate')
            messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')

        return render(request, 'login.html', {'login_form': login_form})

class SelectBranchView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        branches = Restaurant_Chain_Branch.objects.filter(id_restaurant_chain=request.user)
        return render(request, 'select_branch.html', {'branches': branches})

    def post(self, request):
        branch_id = request.POST.get('branch_id')
        branch = get_object_or_404(Restaurant_Chain_Branch, id=branch_id, id_restaurant_chain=request.user)
        request.user.selected_branch = branch
        request.user.save()
        return redirect('inventory')

class CreateBranchView(View):
    def post(self, request):
        user = request.user
        branches = Restaurant_Chain_Branch.objects.filter(id_restaurant_chain=user)
        restaurant_chain = get_object_or_404(Restaurant_Chain, email=user.email)

        image = request.FILES['branch_image']
        branch_name = request.POST['branch_name']
        address = request.POST['branch_address']

        if restaurant_chain.branches.filter(address=address).exists():
            messages.error(request, 'Branch with same address already exists')
            return render(request, 'select_branch.html', {'branches': branches})

        Restaurant_Chain_Branch.objects.create(
            id_restaurant_chain=restaurant_chain,
            image=image,
            branch=branch_name,
            address=address
        )

        messages.success(request, 'Branch created successfully')
        return redirect('select_branch')

    def get(self, request):
        return redirect('select_branch')
